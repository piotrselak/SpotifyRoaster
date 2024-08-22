from pydantic import BaseModel


class AccessTokenBody(BaseModel):
    access_token: str
    token_type: str
    scope: str
    expires_in: int
    refresh_token: str