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
from typing import Dict, Optional
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
    player: str
    guess: str

scoreboard: Dict[str, int] = {}
current_query: Optional[str] = None
current_lyrics: Optional[str] = None
current_snippet: Optional[str] = None
round_active: bool = False

# Snippet'ları static olarak sun
app.mount("/snippets", StaticFiles(directory="static/snippets"), name="snippets")



@app.get("/api/snippet")
def get_random_snippet():
    global current_query, current_snippet, current_lyrics, round_active

    if round_active and current_snippet:
        return {
            "query": current_query,
            "snippet_url": current_snippet,
            "duration": 12,
            "lyrics": current_lyrics,
        }

    query = random.choice(search_queries)
    print(f"🎲 Seçilen şarkı: {query}")

    try:
        audio_url = get_best_audio_url_from_youtube(query)

        filename = f"snippet_{uuid.uuid4()}.mp3"
        output_path = os.path.join("static/snippets", filename)
        generate_snippet_from_url(audio_url, duration=12, output_path=output_path)

        if "-" in query:
            title, artist = query.split("-", 1)
        elif " " in query:
            title, artist = query.rsplit(" ", 1)
        else:
            title, artist = query, ""

        lyrics = get_lyrics_by_search(artist.strip(), title.strip())
        print("🎶 Lyrics ilk 200 karakter:", lyrics[:200] if lyrics else "Yok")

        current_query = query
        current_snippet = f"/snippets/{filename}"
        current_lyrics = lyrics if lyrics else "Lyrics bulunamadı."
        round_active = True

        return {
            "query": current_query,
            "snippet_url": current_snippet,
            "duration": 12,
            "lyrics": current_lyrics,
        }

    except Exception as e:
        return {"error": str(e)}



@app.post("/api/check")
def check_guess(data: GuessRequest):
    global round_active, scoreboard, current_query

    guess = data.guess.lower().strip()
    player = data.player

    if player not in scoreboard:
        scoreboard[player] = 0

    correct = False
    winner = None

    if current_query:
        answer = current_query.lower()
        if guess in answer or answer in guess:
            correct = True
            if round_active:
                scoreboard[player] += 1
                winner = player
                round_active = False

    return {"correct": correct, "winner": winner, "scoreboard": scoreboard}

app.mount(
    "/", 
    StaticFiles(directory=os.path.join(os.path.dirname(__file__), '..', 'frontend'), html=True), 
    name="frontend"
)
