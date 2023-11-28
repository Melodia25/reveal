from fastapi import FastAPI, Depends, UploadFile
from typing import Annotated

from entity import SessionRequest, SessionResponse, ResponseModel, TokenHeaders, TokenAuthorization
from login import get_access_token, set_session_data, get_user_info
from service import transcribe

app = FastAPI()

UserDep = Annotated[TokenAuthorization, get_user_info]


@app.post("/login")
async def login(session_request: SessionRequest):
    data = get_access_token(session_request.email, session_request.password)
    response = SessionResponse(
        access_token=data.access_token,
        refresh_token=data.refresh_token,
        expires_in=data.expires_in,
        expires_at=data.expires_at
    )
    return response


@app.post("/refresh")
async def refresh(tokens: TokenHeaders):
    return {"data": set_session_data(tokens)}


@app.post("/transcribe")
async def transcribe(audio: UploadFile, user: UserDep = Depends(get_user_info), transcript=Depends(transcribe)):
    if user is not None:
            return transcript
    else:
        return {"error": user}
