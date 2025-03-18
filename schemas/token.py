from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str
    username: str
    email: str


class TokenData(BaseModel):
    username: str | None = None
