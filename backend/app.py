import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from audio_utils import generate_snippet_from_url
from youtube_search import get_best_audio_url_from_youtube
import random
import os
import uuid
import sys
from pydantic import BaseModel
from fastapi import Request
from lyrics_scraper import get_lyrics_by_search

# Arama listesi
search_queries = [
    "Blinding Lights-The Weeknd",
    "Shape of You-Ed Sheeran",
    "Believer-Imagine Dragons",
    "Levitating-Dua Lipa",
    "Bad Guy-Billie Eilish",
    "Adventure of a Lifetime-Coldplay"
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class GuessRequest(BaseModel):
    guess: str
    answer: str

# Snippet'ları static olarak sun
app.mount("/snippets", StaticFiles(directory="static/snippets"), name="snippets")



@app.get("/api/snippet")
def get_random_snippet():
    query = random.choice(search_queries)
    print(f"🎲 Seçilen şarkı: {query}")

    try:
        audio_url = get_best_audio_url_from_youtube(query)

        # Snippet oluştur
        filename = f"snippet_{uuid.uuid4()}.mp3"
        output_path = os.path.join("static/snippets", filename)
        generate_snippet_from_url(audio_url, duration=12, output_path=output_path)

        # Şarkı sözlerini çek (artist + title ayrımı için parse etmen gerekebilir)
        if "-" in query:
            title, artist = query.split("-", 1)
        elif " " in query:
            title, artist = query.rsplit(" ", 1)
        else:
            title, artist = query, ""

        lyrics = get_lyrics_by_search(artist.strip(), title.strip())
        print("🎶 Lyrics ilk 200 karakter:", lyrics[:200] if lyrics else "Yok")

        return {
            "query": query,
            "snippet_url": f"/snippets/{filename}",
            "duration": 12,
            "lyrics": lyrics if lyrics else "Lyrics bulunamadı."
        }

    except Exception as e:
        return {"error": str(e)}



@app.post("/api/check")
def check_guess(data: GuessRequest):
    guess = data.guess.lower().strip()
    answer = data.answer.lower().strip()

    correct = guess in answer or answer in guess
    return {"correct": correct}

app.mount(
    "/", 
    StaticFiles(directory=os.path.join(os.path.dirname(__file__), '..', 'frontend'), html=True), 
    name="frontend"
)
