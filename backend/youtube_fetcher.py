import yt_dlp
from pydub import AudioSegment
import os
import uuid
import json
import time

# Kaydedilecek dosya klasörü
MEDIA_DIR = "media"
os.makedirs(MEDIA_DIR, exist_ok=True)

# Şarkı listesi
search_queries = [
    "Blinding Lights The Weeknd",
    "Shape of You Ed Sheeran",
    "Dance Monkey Tones and I",
    "Believer Imagine Dragons",
    "Levitating Dua Lipa",
    "Lose Yourself Eminem",
    "Bad Guy Billie Eilish",
    "Adventure of a Lifetime Coldplay",
    "Hymn for the Weekend Coldplay",
    "One More Night Maroon 5",
    "Sorry Justin Bieber",
    "Hello Adele",
    "Somebody That I Used to Know Gotye",
    "Rolling in the Deep Adele"
]

# Şarkıyı indir ve ilk 30 saniyesini kaydet
def download_and_trim_youtube_audio(query):
    temp_id = str(uuid.uuid4())
    output_file = f"{temp_id}.mp3"
    search_url = f"ytsearch1:{query}"

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_file,
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(search_url, download=True)
            title = info['entries'][0]['title']
            webpage_url = info['entries'][0]['webpage_url']
        except Exception as e:
            print(f"❌ İndirme hatası: {e}")
            return None

    try:
        audio = AudioSegment.from_file(output_file)
        first_30_sec = audio[:30 * 1000]  # 30 saniye
        trimmed_name = query.lower().replace(" ", "_").replace("/", "_") + ".mp3"
        trimmed_path = os.path.join(MEDIA_DIR, trimmed_name)
        first_30_sec.export(trimmed_path, format="mp3")
        os.remove(output_file)
        print(f"✅ {query} -> {trimmed_path}")
        return {
            "name": title,
            "query": query,
            "youtube_url": webpage_url,
            "file": trimmed_path
        }
    except Exception as e:
        print(f"❌ Kırpma hatası: {e}")
        return None

if __name__ == "__main__":
    collected = []
    for q in search_queries:
        print(f"🎵 Aranıyor: {q}")
        result = download_and_trim_youtube_audio(q)
        if result:
            collected.append(result)
        time.sleep(1)

    with open("songs.json", "w", encoding="utf-8") as f:
        json.dump(collected, f, ensure_ascii=False, indent=2)

    print("🎧 Toplam şarkı sayısı:", len(collected))
