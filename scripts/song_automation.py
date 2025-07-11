import requests
import base64
import json
import time

# Spotify API bilgileri (BURAYI DOLDUR)
CLIENT_ID = ""
CLIENT_SECRET = ""

# Erişim token'ı al
def get_access_token():
    auth_str = f"{CLIENT_ID}:{CLIENT_SECRET}"
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()
    
    response = requests.post("https://accounts.spotify.com/api/token",
        headers={
            "Authorization": f"Basic {b64_auth_str}",
        },
        data={
            "grant_type": "client_credentials"
        }
    )
    response.raise_for_status()
    return response.json()["access_token"]

# Şarkı arayıp preview_url ve meta bilgileri al
def search_song(query, token):
    url = "https://api.spotify.com/v1/search"
    params = {
        "q": query,
        "type": "track",
        "limit": 5  # daha fazla seçenek denemek için
    }
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    items = response.json()["tracks"]["items"]
    
    for track in items:
        if track["preview_url"]:
            return {
                "name": track["name"],
                "artist": track["artists"][0]["name"],
                "preview_url": track["preview_url"],
                "answer_lyrics": ""  # Daha sonra doldur
            }
    return None


# Ana işlem
if __name__ == "__main__":
    # Aranacak şarkı listesi (dilersen buraya daha fazla ekleyebilirsin)
    search_queries = [
        "track:Blinding Lights artist:The Weeknd",
        "track:Shape of You artist:Ed Sheeran",
        "track:Dance Monkey artist:Tones and I",
        "track:Believer artist:Imagine Dragons",
        "track:Levitating artist:Dua Lipa",
        "track:Lose Yourself artist:Eminem",
        "track:Bad Guy artist:Billie Eilish",
        "track:Adventure of a Lifetime artist:Coldplay",
        "track:Hymn for the Weekend artist:Coldplay",
        "track:One More Night artist:Maroon 5",
        "track:Sorry artist:Justin Bieber",
        "track:Hello artist:Adele",
        "track:Somebody That I Used to Know artist:Gotye",
        "track:Rolling in the Deep artist:Adele",
        "track:Counting Stars artist:OneRepublic",
        "track:Thunder artist:Imagine Dragons",
        "track:Take Me to Church artist:Hozier",
        "track:Stressed Out artist:Twenty One Pilots",
        "track:Radioactive artist:Imagine Dragons",
        "track:Let Her Go artist:Passenger"
    ]
    token = get_access_token()
    collected_songs = []

    for query in search_queries:
        print(f"🎵 Aranıyor: {query}")
        try:
            result = search_song(query, token)
            if result:
                collected_songs.append(result)
                print(f"✅ Bulundu: {result['artist']} - {result['name']}")
            else:
                print(f"❌ Önizleme bulunamadı: {query}")
        except Exception as e:
            print(f"⚠️ Hata: {e}")
        time.sleep(1)  # Spotify rate-limit'e yakalanmamak için

    # JSON dosyasına yaz
    with open("valid_songs.json", "w", encoding="utf-8") as f:
        json.dump(collected_songs, f, ensure_ascii=False, indent=2)
    print("✅ Tamamlandı. Dosya: valid_songs.json")
    # Şarkıların preview_url'lerini kontrol et
    for song in collected_songs:
        if not song["preview_url"]:
            print(f"❌ Şarkı önizleme URL'si bulunamadı: {song['name']} - {song['artist']}")
        else:
            print(f"✅ Şarkı önizleme URL'si mevcut: {song['name']} - {song['artist']}")
