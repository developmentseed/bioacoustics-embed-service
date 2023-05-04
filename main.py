# main.py
import numpy as np
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from chirp.inference import models

app = FastAPI()

class AudioInput(BaseModel):
    audio_base64: str

@app.get("/")
def health():
    return {"status": "success"}

@app.post("/predict")
async def predict_audio(audio_file: UploadFile = File(...)):
    with open(f"temp_{audio_file.filename}", "wb") as buffer:
        content = await audio_file.read()
        # save the wav for now
        buffer.write(content)

    return {"filename": audio_file.filename}
