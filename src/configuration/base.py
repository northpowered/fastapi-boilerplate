from pydantic import (BaseModel, ValidationError)
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
            error = ex.errors()[0]
            logger.error(f"{section_name} | {error.get('loc')[0]} | {error.get('msg')}") # type: ignore
            os._exit(0)
                        