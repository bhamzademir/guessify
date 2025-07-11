import json
import random
import requests
import tempfile
import uuid
import os
from playsound import playsound, PlaysoundException

# 1. Şarkı listesini yükle
try:
    with open("backend/data/songs.json", "r", encoding="utf-8") as f:
        songs = json.load(f)
except FileNotFoundError:
    print("❌ Şarkı listesi dosyası bulunamadı.")
    exit(1)
except json.JSONDecodeError:
    print("❌ songs.json dosyası bozuk ya da hatalı formatta.")
    exit(1)

# 2. Rastgele bir şarkı seç
song = random.choice(songs)
print(f"🎵 Şarkı çalınıyor: {song['artist']} - {song['name']}")

# 3. Şarkıyı indir ve geçici dosyaya kaydet
try:
    response = requests.get(song["preview_url"])
    response.raise_for_status()
except requests.RequestException as e:
    print(f"❌ Şarkı indirilemedi: {e}")
    exit(1)

# 4. Geçici dosya oluştur
with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
    tmp_file.write(response.content)
    filename = tmp_file.name

# 5. Şarkıyı oynat
try:
    playsound(filename)
except PlaysoundException as e:
    print(f"❌ Şarkı oynatılamadı (playsound hatası): {e}")
    print("🔧 Olası neden: codec veya dosya uyumsuzluğu. Dosya bozuk olabilir.")
    os.remove(filename)
    exit(1)
except Exception as e:
    print(f"❌ Beklenmedik bir hata oluştu: {e}")
    os.remove(filename)
    exit(1)

# 6. Kullanıcıdan tahmin al
guess = input("📢 Şarkının sözünü tahmin et: ").strip().lower()

# 7. Cevabı kontrol et
correct_answer = song["answer_lyrics"].strip().lower()
if correct_answer in guess or guess in correct_answer:
    print("✅ Doğru tahmin! Aferin!")
else:
    print(f"❌ Yanlış. Doğru cevap: '{song['answer_lyrics']}'")

# 8. Geçici dosyayı sil
try:
    os.remove(filename)
except OSError:
    print(f"⚠️ Geçici dosya silinemedi: {filename}")
