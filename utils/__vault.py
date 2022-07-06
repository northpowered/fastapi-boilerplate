from configuration import config
from loguru import logger
from utils.telemetry import tracer
from async_hvac import AsyncClient, exceptions
import aiohttp
from pydantic import BaseModel
import os

class Vault():

    class DBCredsModel(BaseModel):
        username: str
        password: str


    def __init__(self):
        pass

            
    async def init(self):
        if config.vault.is_enabled:
            if await self.check_vault_state():
                logger.info(f"Vault instance is ready")
            else:
                logger.critical(f"Vault instance creation failed")
        else:
            logger.info(f"Vault module is inactive")

    async def testfoo(self):
        async with Vault.get_instance() as client:
            print(type(client))
            q = await client.is_authenticated()
            print(f" testfoo {q}")
            return q

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
                async with Vault.get_instance() as client:
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

    @staticmethod
    async def unseal_vault(vault_instance: AsyncClient)->bool:
        logger.warning('Vault instance is sealed, trying to unseal...')
        try:
            assert config.vault.vault_unseal_keys,"You should define [vault_unseal_keys] file in config file"
            keys_file = str(config.vault.vault_unseal_keys)
            with open(keys_file, 'r') as f:
                keys = f.readlines()
                assert len(keys)>=3,"You should define 3 or more unseal keys"
                await vault_instance.unseal_multi(keys)
        except FileNotFoundError as ex:
            logger.critical(f'File with unsealing vault keys {keys_file} not found')
        except PermissionError as ex:
            logger.critical(f'Cannot open {keys_file}, permission denied')
        except AssertionError as ex:
            logger.critical(ex)
        except exceptions.InvalidRequest as ex:
            logger.critical(f'Broken keys structure in {keys_file}')
        
        if await vault_instance.is_sealed():
            logger.critical('Vault unsealing process failed')
            return False
        else:
            logger.info('Vault instance was successfully unsealed')
            return True




    @staticmethod
    async def check_vault_state()->bool:
        """
        Method for checking vault service state with separate
        client session
        """
        try:
            async with Vault.get_instance() as client:
                try:
                    if config.vault.is_unsealing_available and await client.is_sealed():
                        assert await Vault.unseal_vault(client),"Unable to unseal vault"
                        

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
            



    @staticmethod
    def get_instance()->AsyncClient:
        instance = AsyncClient()
        scheme = "http"
        if config.vault.is_tls:
            scheme = "https"
        url = f"{scheme}://{config.vault.vault_host}:{config.vault.vault_port}"
        match config.vault.vault_auth_method:
            case "token":
                instance = AsyncClient(url=url, token=config.vault.vault_token)
            case _:
                pass
        return instance
