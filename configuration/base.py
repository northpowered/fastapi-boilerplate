from pydantic import (BaseSettings, BaseModel,
                      ValidationError, validator, Field,
                      PostgresDsn)
from loguru import logger

import os

class BaseSectionModel(BaseModel):

    def __repr__(self) -> str:
        return f"<FastAPIConfigurationSection object at {hex(id(self))}>"

    def load(self, section_data: dict, section_name: str):
        try:
            return self.parse_obj(section_data)
        except KeyError:
            logger.error(f'Missed {section_name} section in config file')
            os._exit(0)
        except ValidationError as ex:
            logger.error(ex.errors())
            os._exit(0)
                        