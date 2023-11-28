import os

from fastapi import UploadFile
from openai import  OpenAI
import tempfile
import shutil
client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=os.getenv("KEY_OPENAI"),
)



async def transcribe(audio: UploadFile):

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
        temp_file_name = temp_file.name
        await audio.seek(0)  # Rewind to the beginning of the file
        shutil.copyfileobj(audio.file, temp_file)


    # Now pass this byte stream to the OpenAI API
    with open(temp_file_name, "rb") as file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=file,
            response_format="verbose_json"
        )
    os.remove(temp_file_name)
    return transcript