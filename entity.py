from typing import Union, Dict, Optional, Any

from pydantic import BaseModel, EmailStr

class ResponseModel(BaseModel):
    data: Optional[Any] = None
    error: Optional[bool] = False
    message: Optional[str] = None
class SessionResponse(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int
    expires_at: Union[int, None] = None


class SessionRequest(BaseModel):
    email: EmailStr
    password: str




class TokenHeaders(BaseModel):
    Authorization: str
    Refresh_Token: str
