import configuration
from .sections import (
    MainSectionConfiguration,
    AdminGUISectionConfiguration,
    SecuritySectionConfiguration,
    ServerSectionConfiguration,
    VaultSectionConfiguration,
    DatabaseSectionConfiguration,
    TelemetrySectionConfiguration
)
from pydantic import BaseSettings
import configparser
from loguru import logger
class Configuration(BaseSettings):

    def __repr__(self) -> str:
        return f"<FastAPIConfiguration object at {hex(id(self))}>"

    main: MainSectionConfiguration = MainSectionConfiguration()
    admin_gui: AdminGUISectionConfiguration = AdminGUISectionConfiguration()
    server: ServerSectionConfiguration = ServerSectionConfiguration()
    vault: VaultSectionConfiguration = VaultSectionConfiguration()
    database: DatabaseSectionConfiguration = DatabaseSectionConfiguration()
    telemetry: TelemetrySectionConfiguration = TelemetrySectionConfiguration()
    security: SecuritySectionConfiguration = SecuritySectionConfiguration()

    def load(self, filename: str, filetype: str | None = None):
        raw_data: dict = dict()
        try:
            file_extention = filename.split('.')[1]
        except IndexError:
            print('index error')
        else:
            print(file_extention)
        match file_extention:
            case 'ini': raw_data = Configuration.ini_reader(filename)
        #print(dict(Configuration.ini_reader(filename)['Main']))
        print(raw_data)
        config = configparser.ConfigParser()
        config.read(filename)
        self.read_from_configparcer(config)
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

    def read_from_configparcer(self, configparcer: configparser.ConfigParser):

        self.main = self.main.load(configparcer,'Main')
        self.admin_gui = self.admin_gui.load(configparcer,'AdminGUI')
        self.server = self.server.load(configparcer,'Server')
        self.vault = self.vault.load(configparcer,'Vault')
        self.database = self.database.load(configparcer,'Database')
        self.telemetry = self.telemetry.load(configparcer,'Telemetry')
        self.security = self.security.load(configparcer,'Security')