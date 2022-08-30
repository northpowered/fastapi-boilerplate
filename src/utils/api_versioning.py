from fastapi import APIRouter as _APIRouter
from typing import NamedTuple
class APIVersion(NamedTuple):

    major: int = 1
    minor: int | None = None

    def __str__(self)->str:
        if self.minor is not None:
            return f"{self.major}_{self.minor}"
        else:
            return f"{self.major}"

class APIRouter(_APIRouter):
    def __init__(self, version: APIVersion | None=None, **kwargs):
        super().__init__(**kwargs)
        if version:
            self.prefix = f"/v{version}{self.prefix}"

