from .base import BaseSectionModel
from  pydantic import (validator,PostgresDsn)
import ipaddress
import datetime
from loguru import logger
from typing import Any
import sys
import re
import os
class MainSectionConfiguration(BaseSectionModel):

    application_mode: str = 'prod'
    log_level: str = 'INFO'
    log_destination: str = 'stdout'
    log_in_json: int = 0
    log_sql: int = 0
    timezone: int = +3
    enable_swagger: int = 1
    swagger_doc_url: str = '/doc'
    swagger_redoc_url: str = '/redoc'

    @validator('application_mode')
    def check_appmode(cls, v):
        assert isinstance(v, str)
        assert v in ['prod','dev']
        return v
    
    @validator('log_level')
    def check_loglevel(cls, v):
        assert isinstance(v, str)
        assert v.upper() in ['DEBUG','INFO','WARNING','ERROR','CRITICAL']
        return v.upper()
    
    @validator('log_destination')
    def check_logdestination(cls, v):
        assert isinstance(v, str)
        assert v == 'stdout' or os.path.isfile(v)
        return v

    @validator('log_in_json')
    def check_loginjson(cls,v):
        assert isinstance(v, int)
        assert v in [0,1]
        return v
        
    @validator('log_sql')
    def check_logsql(cls,v):
        assert isinstance(v, int)
        assert v in [0,1]
        return v

    @validator('enable_swagger')
    def check_enable_swagger(cls,v):
        assert isinstance(v, int)
        assert v in [0,1]
        return v

    @validator('swagger_doc_url','swagger_redoc_url')
    def check_admin_url_slashes(cls,v):
        assert isinstance(v, str)
        assert bool(re.match('/.*',v)),'url MUST starts with /'
        return v

    @property
    def log_sink(self):
        if self.log_destination == 'stdout':
            return sys.stdout
        else:
            return self.log_destination

    @property
    def tz(self)->datetime.timezone:
        return (
            datetime.timezone(
                datetime.timedelta(
                    hours=self.timezone
                )
            )
        )

    @property
    def is_swagger_enabled(self)->bool:
        return bool(self.enable_swagger)

    @property
    def doc_url(self)->str | None:
        if self.is_swagger_enabled:
            return self.swagger_doc_url
        else:
            return None

    @property
    def redoc_url(self)->str | None:
        if self.is_swagger_enabled:
            return self.swagger_redoc_url
        else:
            return None

    @property
    def is_prod_mode(self)->bool:
        return self.application_mode == 'prod'


class AdminGUISectionConfiguration(BaseSectionModel):

    admin_enable: int = 1
    admin_url: str = '/admin/'

        
    @validator('admin_enable')
    def check_admin_enable(cls,v):
        assert isinstance(v, int)
        assert v in [0,1]
        return v

    @validator('admin_url')
    def check_admin_url_slashes(cls,v):
        assert isinstance(v, str)
        assert bool(re.match('/.*/',v)),'url MUST starts and end with /'
        return v


    @property
    def is_admin_gui_enable(self)->bool:
        return bool(self.admin_enable)



class ServerSectionConfiguration(BaseSectionModel):

    bind_address: str = '127.0.0.1'
    bind_port: int = 8000
    base_url:str = 'localhost'

    @validator('bind_port')
    def check_port(cls, v):
        assert isinstance(v, int)
        assert v in range(0,65535)
        return v

    @validator('bind_address')
    def check_address(cls,v):
        try:
            ipaddress.ip_address(v)
        except ValueError:
            assert v == 'localhost'
            v = '127.0.0.1'
        finally:
            return v

class DatabaseSectionConfiguration(BaseSectionModel):

    db_driver: str = 'postgresql+asyncpg'
    db_host: str = '127.0.0.1'
    db_port: int = 5432
    db_name: str = 'enforcer'
    db_username: str = 'enforcer'
    db_password: str = 'enforcer'

    db_vault_enable: int = 0
    db_vault_role: str = 'myrole'
    db_vault_static: int = 1
    db_vault_storage: str = 'database'

    connection_string: str = "empty"

    engine: Any | None = None

    def set_connection_string(self, s: str):
        self.connection_string = s
    

    def get_engine(self):
        return self.engine

    def set_engine(self, new_engine):
        self.engine = new_engine


    @validator('db_driver')
    def check_driver(cls,v):
        assert v in ['postgresql+asyncpg','postgresql']
        return v

    @validator('db_port')
    def check_port(cls, v):
        assert isinstance(v, int)
        assert v in range(0,65535)
        return v

    @validator('db_host')
    def check_address(cls,v):
        try:
            ipaddress.ip_address(v)
        except ValueError:
            assert v=='localhost'
            v='127.0.0.1'
        finally:
            return v

    @validator('db_vault_enable')
    def check_vault_enable(cls,v):
        assert v in [0,1]
        return v

    @validator('db_vault_static')
    def check_vault_static(cls,v):
        assert v in [0,1]
        return v

    @property
    def is_vault_enable(self)->bool:
        return bool(self.db_vault_enable)


    @property
    def is_vault_static(self)->bool:
        return bool(self.db_vault_static)

    
    def build_connection_string(self, username:str | None = None, password:str | None = None)->str:
        if not username or not password:
            logger.debug('Using plaintext credentials')
            username = self.db_username
            password = self.db_password
        return PostgresDsn.build(
            scheme=self.db_driver,
            host=self.db_host,
            port=str(self.db_port),
            path=f'/{self.db_name}',
            user=username,
            password=password,
            )

class VaultSectionConfiguration(BaseSectionModel):

    vault_enable: int = 0
    vault_host: str = 'localhost'
    vault_port: int = 8200
    vault_disable_tls: int = 0
    vault_auth_method: str = 'token'
    vault_token: str | None = None
    vault_credentials: str | None = None
    vault_keyfile_type: str | None = None
    vault_try_to_unseal: int = 0
    vault_unseal_keys: str | None = None



    @validator('vault_enable')
    def check_enabling(cls,v):
        assert v in [0,1]
        return v

    @validator('vault_host')
    def check_address(cls,v):
        try:
            ipaddress.ip_address(v)
        except ValueError:
            assert v=='localhost'
            v='127.0.0.1'
        finally:
            return v

    @validator('vault_port')
    def check_port(cls, v):
        assert isinstance(v, int)
        assert v in range(0,65535)
        return v

    @validator('vault_disable_tls')
    def check_tls(cls,v):
        assert v in [0,1]
        return v

    @validator('vault_auth_method')
    def check_auth_method(cls,v):
        assert v in ['token']
        return v

    @validator('vault_keyfile_type')
    def check_keyfile_type(cls,v):
        if v:
            assert v in ['json','keys']
        return v

    @validator('vault_try_to_unseal')
    def check_try_to_unseal(cls,v):
        assert v in [0,1]
        return v

    @property
    def is_enabled(self)->bool:
        return bool(self.vault_enable)

    @property
    def is_tls(self)->bool:
        return not bool(self.vault_disable_tls)

    @property
    def is_unsealing_available(self)->bool:
        return bool(self.vault_try_to_unseal)

class TelemetrySectionConfiguration(BaseSectionModel):

    enable: int = 1
    agent_type: str = 'jaeger'
    agent_host: str = '127.0.0.1'
    agent_port: int = 6831

    @validator('enable')
    def check_status(cls,v):
        assert v in [0,1]
        return v

    @validator('agent_type')
    def check_type(cls,v):
        assert v in ['jaeger']
        return v

    @validator('agent_port')
    def check_port(cls, v):
        assert isinstance(v, int)
        assert v in range(0,65535)
        return v

    @validator('agent_host')
    def check_address(cls,v):
        try:
            ipaddress.ip_address(v)
        except ValueError:
            assert v=='localhost'
            v='127.0.0.1'
        finally:
            return v

    @property
    def is_active(self)->bool:
        return bool(self.enable)

class SecuritySectionConfiguration(BaseSectionModel):

    enable_rbac: int = 1

    @validator('enable_rbac')
    def check_enable_rbac(cls,v):
        assert v in [0,1]
        return v

    @property
    def is_rbac_enabled(self)->bool:
        return bool(self.enable_rbac)
