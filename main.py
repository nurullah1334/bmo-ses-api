from fastapi import FastAPI
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
import edge_tts

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "BMO Ses API Aktif!"}

@app.get("/tts")
async def generate_bmo_voice(text: str = "Merhaba Bimo!"):
    communicate = edge_tts.Communicate(
        text=text,
        voice="tr-TR-EmelNeural",
        pitch="+38Hz",
        rate="+14%"
    )
    audio_bytes = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_bytes += chunk["data"]
    return Response(content=audio_bytes, media_type="audio/mpeg")
