from fastapi import FastAPI, Depends, UploadFile, File
from typing import Annotated

from entity import SessionRequest, SessionResponse, ResponseModel
from login import get_access_token, set_session_data
from service import transcribe

app = FastAPI()

SessionDep = Annotated[ResponseModel, set_session_data]

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


@app.post("/prueba")
async def transcribe(audio:UploadFile, session: SessionDep= Depends(set_session_data),  transcript=Depends(transcribe)):
    if not session.error:
        if audio.content_type != 'audio/mpeg':
            return {"error": "El archivo debe ser un MP3."}

        # Validar el tamaño del archivo (25 MB = 25 * 1024 * 1024 bytes)
        if audio.size > 25 * 1024 * 1024:
            return {"error": "El archivo no debe superar los 25 MB."}

        if audio.content_type != 'audio/mpeg':
            return {"error": "El archivo debe ser un MP3."}

        return transcript
    else:
        return session