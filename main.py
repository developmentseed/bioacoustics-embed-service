# main.py
import numpy as np
import warnings
import io
import librosa
from absl import logging
from pathlib import Path
from fastapi import FastAPI, File, UploadFile
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from chirp.inference import models
from fastapi.encoders import jsonable_encoder

app = FastAPI()

SAVED_MODEL_PATH = str(Path('.').resolve())
model_configs = {
    'hop_size_s': 5.0,
    'sample_rate': 32000,
    'window_size_s': 5.0
}

print(model_configs)
model = models.TaxonomyModelTF(model_configs['sample_rate'], SAVED_MODEL_PATH, model_configs['hop_size_s'], model_configs['window_size_s'])

class AudioInput(BaseModel):
    audio_base64: str

@app.get("/")
def health():
    return {"status": "success"}

@app.post("/embed")
async def predict_audio(audio_file: UploadFile = File(...)):
    with open(f"temp_{audio_file.filename}", "wb") as buffer:
        content = await audio_file.read()
        # save the wav for now
        # buffer.write(content)
        buffer = io.BytesIO(content)
        print('reading audtio...')
        audio = load_audio(buffer)
        outputs = None
        if (audio.any()):
            # waveform = np.zeros(5 * 32000, dtype=np.float32)
            try:
                print('preparing embedding...')
                outputs = model.embed(audio)
                print(outputs.embeddings.shape)
            except Exception as e:
                logging.error('Failed to prepare embeddings', e)
                raise HTTPException(500, detail=f'{e}')

            return {
                "embedding": jsonable_encoder(outputs.embeddings.tolist())
                }

# based on load_audio method from chirp/embedlib.py
def load_audio(buffer) -> np.ndarray | None:
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        try:
            audio, _ = librosa.load(
                buffer, sr=model_configs['sample_rate'], res_type='polyphase'
            )
        except Exception as inst:  # pylint: disable=broad-except
            # We have no idea what can go wrong in librosa, so we catch a broad
            # exception here.
            logging.warning(
                'The audio at %s could not be loaded. The exception was (%s)',
                filepath,
                inst,
            )
            return None
        while len(audio.shape) > 1:
            # In case of multi-channel audio, take the first channel.
            audio = audio[0]
        return audio