from configuration import config
from loguru import logger
from utils.telemetry import tracer
from async_hvac import AsyncClient, exceptions
import aiohttp
from pydantic import BaseModel
import os
import json
import ctypes
class Vault():

    class DBCredsModel(BaseModel):
        username: str
        password: str

    class UnsealingKeys(BaseModel):
        keys: list[str] | None
        keys_base64: list[str] = list()
        root_token: str | None

    class VaultAuth(BaseModel):
        auth_method: str | None = None
        token: str| None = None
        credentials: str | None = None


    def __init__(self):
        self.unsealing_keys: self.UnsealingKeys = self.UnsealingKeys()
        self.auth: self.VaultAuth = self.VaultAuth()

    def __repr__(self) -> str:
        return f"<VaultFastAPIInstance object at {hex(id(self))}>"

    async def init(self):
        if config.vault.is_enabled:
            self.load_auth_data()
            if await self.check_vault_state():
                logger.info(f"Vault instance is ready")
            else:
                logger.critical(f"Vault instance creation failed")
        else:
            logger.info(f"Vault module is inactive")
        
    def get_auth_token(self)->str | None:
        if config.vault.vault_token:
            return config.vault.vault_token
        if self.unsealing_keys:
            return self.unsealing_keys.root_token
        logger.critical(f'Cannot obtain Vault auth token')
        return None
            
    def load_auth_data(self)->None:
        auth_method: str = config.vault.vault_auth_method
        self.auth.auth_method = auth_method
        if config.vault.vault_keyfile_type:
            self.unsealing_keys = self.open_keys_file(
                filetype=config.vault.vault_keyfile_type,
                filename=config.vault.vault_unseal_keys # type: ignore #TODO prev field check in config-loader
            )
        match auth_method:
            case 'token':
                token = self.get_auth_token()
                self.auth.token = token
            case _:
                logger.critical(f'Unknown vault auth method')
        return None

    def open_keys_file(self,filetype:str, filename: str)->UnsealingKeys: # type: ignore
        try:
            with open(filename,'r') as f:
                if filetype=='json':
                    data = json.load(f)
                    return self.UnsealingKeys(**data)
                if filetype=='keys':
                    data = f.readlines()
                    return self.UnsealingKeys(keys_base64=data)
        except FileNotFoundError as ex:
            logger.critical(f'File with unsealing vault keys {filename} not found')
        except PermissionError as ex:
            logger.critical(f'Cannot open {filename}, permission denied')

    async def get_db_creds(self, role_name:str, static:bool=True, storage_name:str='database')->DBCredsModel:
        with tracer.start_as_current_span("security:Vault:get_db_creds") as span:
            span.set_attribute("role.name", role_name)
            span.set_attribute("role.static", static)
            span.set_attribute("role.storage", storage_name)
            creds_type = 'static-creds'
            if not static:
                creds_type = 'creds'
            data = await self._action('read',f'{storage_name}/{creds_type}/{role_name}')
            try:
                assert data,"Unable to obtain db credential from Vault"
            except AssertionError as ex:
                logger.critical(ex)
                os._exit(0)
            creds = self.DBCredsModel.parse_obj(data)
            return creds

    async def request_certificate(self,role_name: str, storage_name: str, common_name: str, cert_ttl:str)->dict | None:
        with tracer.start_as_current_span("security:Vault:request_certificate") as span:
            span.set_attribute("role.name", role_name)
            span.set_attribute("role.storage", storage_name)
            payload:dict = {
                'common_name':common_name,
                'ttl':cert_ttl
            }
            data = await self._action('write',f'{storage_name}/issue/{role_name}',payload=payload)
            try:
                assert data,"Unable to request certificate from Vault"
            except AssertionError as ex:
                logger.warning(ex)
                return None
            return data

    async def _action(self, action_type, route, payload = None):
        with tracer.start_as_current_span("security:Vault:_action") as span:
            span.set_attribute("action.type", action_type)
            span.set_attribute("action.route", route)
            if payload:
                span.set_attribute("action.payload", payload)
            try:
                async with self.get_instance() as client:
                    try:
                        assert not await client.is_sealed(),"Vault storage is sealed"
                        assert await client.is_initialized(),"Vault storage is not initialized"
                        assert await client.is_authenticated(),"Vault authentication error"
                        match action_type:
                            case 'read':
                                return await self._read(client,route)
                            case 'write':
                                return await self._write(client,route,**payload)
                            case _:
                                logger.error(f"Unknown Vault operation {action_type}")
                    except (AssertionError, aiohttp.client_exceptions.ClientConnectorError) as ex:
                        logger.error(ex)
                        raise AttributeError
            except AttributeError:
                logger.error(f"Vault instance creation failed")
                return False

    async def _read(self, instance: AsyncClient, route:str):
        with tracer.start_as_current_span("security:Vault:_read") as span:
            try:
                resp = await instance.read(route)
                assert resp,"Empty responce"
                data = resp.get('data')
                assert data,"Empty data field"
            except (exceptions.InvalidRequest, AssertionError) as ex:
                logger.error(f"Vault read operation error: {ex}")
                return None
            else:
                return data

    async def _write(self, instance: AsyncClient, route:str,**kwargs):
        with tracer.start_as_current_span("security:Vault:_write") as span:
            try:
                resp = await instance.write(route,**kwargs)
                assert resp,"Empty responce"
                data = resp.get('data')
                assert data,"Empty data field"
            except (exceptions.InvalidRequest, AssertionError) as ex:
                logger.error(f"Vault write operation error: {ex}")
                return None
            else:
                return data

    
    async def unseal_vault(self,vault_instance: AsyncClient)->bool:
        logger.warning('Vault instance is sealed, trying to unseal...')
        try:
            keys: list = self.unsealing_keys.keys_base64
            await vault_instance.unseal_multi(keys)
        except exceptions.InvalidRequest as ex:
            logger.critical(f'Broken keys structure in unsealing_keys file')
        
        if await vault_instance.is_sealed():
            logger.critical('Vault unsealing process failed')
            return False
        else:
            logger.info('Vault instance was successfully unsealed')
            return True




    
    async def check_vault_state(self)->bool:
        """
        Method for checking vault service state with separate
        client session
        """
        
        try:
            async with self.get_instance() as client:
                try:
                    if config.vault.is_unsealing_available and await client.is_sealed():
                        assert await self.unseal_vault(client),"Unable to unseal vault"
                    assert not await client.is_sealed(),"Vault storage is sealed"
                    assert await client.is_initialized(),"Vault storage is not initialized"
                    assert await client.is_authenticated(),"Vault authentication error"
                except AssertionError as ex:
                    logger.error(ex)
                    raise AttributeError
                except aiohttp.client_exceptions.ClientConnectorError as ex:
                    logger.error(ex)
                    raise AttributeError
        except AttributeError:
            logger.error(f"Vault instance creation failed")
            return False
        else:
            logger.debug(f"Vault instance is ready")
            return True
            



    
    def get_instance(self)->AsyncClient:
        instance = AsyncClient()
        scheme = "http"
        if config.vault.is_tls:
            scheme = "https"
        url = f"{scheme}://{config.vault.vault_host}:{config.vault.vault_port}"
        match self.auth.auth_method:
            case "token":
                token = self.auth.token
                instance = AsyncClient(url=url, token=token)
            case _:
                pass
        return instance
