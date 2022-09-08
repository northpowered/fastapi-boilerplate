from pydantic import BaseModel


class Token(BaseModel):
    """READ model for obtaining JWT"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Extracted payload from JWT"""
    username: str | None = None
