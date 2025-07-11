import requests
import base64
import uuid
import json
import os

# === 1. Spotify'dan Token Al ===
def get_spotify_token(client_id, client_secret):
    auth_str = f"{client_id}:{client_secret}"
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()

    headers = {
        "Authorization": f"Basic {b64_auth_str}"
    }

    data = {
        "grant_type": "client_credentials"
    }

    response = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)
    response.raise_for_status()

    token = response.json().get("access_token")
    return token

# === 2. Sanatçıdan top tracks çek ===
def get_top_tracks(artist_name, token):
    search_url = f"https://api.spotify.com/v1/search?q={artist_name}&type=artist&limit=1"
    headers = {
        "Authorization": f"Bearer {token}"
    }

    res = requests.get(search_url, headers=headers)
    res.raise_for_status()

    artist_items = res.json()["artists"]["items"]

    if not artist_items:
        print(f"[!] Artist not found: {artist_name}")
        return []

    artist_id = artist_items[0]["id"]

    top_tracks_url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=TR"
    res = requests.get(top_tracks_url, headers=headers)
    res.raise_for_status()

    tracks = res.json()["tracks"]
    preview_tracks = [track for track in tracks if track["preview_url"]]

    return preview_tracks

# === 3. Şarkı JSON verisi üret ===
def generate_song_data(artist_name, tracks):
    songs = []
    for track in tracks:
        song = {
            "id": str(uuid.uuid4()),
            "name": track["name"],
            "artist": artist_name,
            "preview_url": track["preview_url"],
            "start_time": 0,
            "duration": 10,
            "answer_lyrics": "type the expected lyric here"
        }
        songs.append(song)
    return songs

# === 4. Ana çalıştırma ===
if __name__ == "__main__":
    client_id = "9d799a852b3642deb07216f518be6f4b"
    client_secret = "0a85972e4107440b8db75cbd48cfccd7"

    token = get_spotify_token(client_id, client_secret)

    artist_list = [
        "Adele",
        "Coldplay",
        "Imagine Dragons",
        "The Weeknd",
        "Taylor Swift",
        "Rihanna",
        "Ed Sheeran"
    ]

    all_songs = []

    for artist in artist_list:
        print(f"Fetching songs for: {artist}")
        try:
            tracks = get_top_tracks(artist, token)
            songs = generate_song_data(artist, tracks[:3])  # İlk 3 şarkı yeterli
            all_songs.extend(songs)
        except Exception as e:
            print(f"[!] Error for artist {artist}: {e}")

    os.makedirs("backend/data", exist_ok=True)

    with open("backend/data/songs.json", "w", encoding="utf-8") as f:
        json.dump(all_songs, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Toplam {len(all_songs)} şarkı yazıldı → backend/data/songs.json")
