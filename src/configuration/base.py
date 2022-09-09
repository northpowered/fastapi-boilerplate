from pydantic import (BaseModel, ValidationError)
from loguru import logger


class BaseSectionModel(BaseModel):

    class Config:
        load_failed: bool = False

    def __repr__(self) -> str:
        return f"<FastAPIConfigurationSection object at {hex(id(self))}>"

    def load(self, section_data: dict, section_name: str):
        try:
            return self.parse_obj(section_data)
        except ValidationError as ex:
            error = ex.errors()[0]
            self.Config.load_failed = True
            logger.error(
                f"{section_name} | {error.get('loc')[0]} | {error.get('msg')}"
            )
            return None
