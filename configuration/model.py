import yaml
from .sections import (
    MainSectionConfiguration,
    AdminGUISectionConfiguration,
    SecuritySectionConfiguration,
    ServerSectionConfiguration,
    VaultSectionConfiguration,
    DatabaseSectionConfiguration,
    TelemetrySectionConfiguration
)
from .base import BaseSectionModel
from pydantic import BaseSettings
import configparser
import toml
from loguru import logger
class Configuration(BaseSettings):

    def __repr__(self) -> str:
        return f"<FastAPIConfiguration object at {hex(id(self))}>"

    Main: MainSectionConfiguration = MainSectionConfiguration()
    AdminGUI: AdminGUISectionConfiguration = AdminGUISectionConfiguration()
    Server: ServerSectionConfiguration = ServerSectionConfiguration()
    Vault: VaultSectionConfiguration = VaultSectionConfiguration()
    Database: DatabaseSectionConfiguration = DatabaseSectionConfiguration()
    Telemetry: TelemetrySectionConfiguration = TelemetrySectionConfiguration()
    Security: SecuritySectionConfiguration = SecuritySectionConfiguration()

    def load(self, filename: str, filetype: str | None = None):
        raw_data: dict = dict()
        try:
            file_extention = filename.split('.')[1]
        except IndexError:
            logger.critical('Cannot find config file extention')
        else:
            match file_extention:
                case 'ini': raw_data = Configuration.ini_reader(filename)
                case 'toml': raw_data = Configuration.toml_reader(filename)
                case 'yaml': raw_data = Configuration.yaml_reader(filename)
                case _: logger.critical('Cannot define config file extention')
        self.read_from_dict(raw_data)
        logger.info(f'Configuration was successfully loaded from {filename}')
        
    @staticmethod
    def ini_reader(filename: str)->dict:
        config = configparser.ConfigParser()
        parced_data: dict = dict()
        with open(filename,'r') as f:
            config.read_file(f)
        for section_name in dict(config).keys():
            if section_name != 'DEFAULT':
                section_data: dict = dict(dict(config).get(section_name)) # type: ignore
                parced_data.update({section_name:section_data})
        return parced_data

    @staticmethod
    def toml_reader(filename: str)->dict:
        with open(filename,'r') as f:
            return toml.loads(f.read())

    @staticmethod
    def yaml_reader(filename: str)->dict:
        with open(filename,'r') as f:
            return yaml.load(f,yaml.loader.SafeLoader)

    def read_from_dict(self, raw_data: dict):
        for section_name in self.__fields__:
            section_data: dict = raw_data.get(section_name,dict())
            section: BaseSectionModel = self.__getattribute__(section_name)
            self.__setattr__(
                section_name,
                section.load(
                    section_data,
                    section_name
                )
            ) 