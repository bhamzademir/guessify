import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import requests

def get_lyrics(url):
    options = Options()
    # options.add_argument("--headless")  # Test için kapalı bırak
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    service = Service("C:/Users/bedir/bhd/guessify/scripts/chromedriver.exe")
    #driver = webdriver.Chrome(service=service, options=options)

    try:
        print("🌐 Sayfa açılıyor...")
        """driver.get(url)
        time.sleep(3)

        print("🔍 Lyrics JSON yükleniyor...")
        json_data = driver.execute_script("return window.__PRELOADED_STATE__")

        html_lyrics = json_data["songPage"]["lyricsData"]["body"]["html"]
        lyrics_soup = BeautifulSoup(html_lyrics, "html.parser")"""
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # New Genius layout
        lyrics_divs = soup.find_all("div", attrs={"data-lyrics-container": "true"})
        if lyrics_divs:
            lines = []
            for div in lyrics_divs:
                # data-exclude-selection olan alt divleri çıkar
                for child in div.find_all(attrs={"data-exclude-from-selection": True}):
                    child.decompose()
                text = div.get_text(separator="\n").strip()
                if text:
                    lines.append(text)
            lyrics = "\n".join(lines)
            return lyrics if lyrics else None

        # Old Genius layout
        lyrics_div = soup.find("div", class_="lyrics")
        print("🔍 Lyrics bulunuyor...")
        if lyrics_div:
            return lyrics_div.get_text(separator="\n").strip()

        print("❌ Lyrics bulunamadı.")
        return None

        """for br in lyrics_soup.find_all("br"):
            br.replace_with("\n")

        return lyrics_soup.get_text(separator="\n").strip()"""

    except Exception as e:
        print(f"❌ Hata: {e}")
        return None

    #finally:
        #driver.quit()


"""if __name__ == "__main__":
    url = "https://genius.com/The-weeknd-blinding-lights-lyrics"
    lyrics = get_lyrics(url)
    if lyrics:
        print("🎉 Sözler:")
        print(lyrics)
    else:
        print("❌ Lyrics alınamadı.")

    with open("blinding_lights_lyrics.txt", "w", encoding="utf-8") as f:
        f.write(lyrics)
    print("💾 Sözler dosyaya kaydedildi.")"""

GENIUS_API_TOKEN = "uZGAEBO3dDJujREU0qKOH3iNLQJkp7L7-dGv8Q3Vvvlb4DhLYMTXWX3vplJEzqqa"  # Token'ı ekle
HEADERS = {"Authorization": f"Bearer {GENIUS_API_TOKEN}"}

def search_song_on_genius(artist, title):
    query = f"{artist} {title}"
    url = "https://api.genius.com/search"
    params = {"q": query}
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    hits = response.json()
    #print(hits)
    hits = hits["response"]["hits"]
    print("Aranan şarkı: ", artist, "-", title)
    for hit in hits:
        result = hit["result"]
        result_title = result["title"].lower()
        result_artist = result["primary_artist"]["name"].lower()
        print(f"🎵 Bulunan Şarkı: {result_title} - {result_artist}")

        if artist.lower() in result_artist and title.lower() in result_title:
            return result["url"]
    return None


def get_lyrics_by_search(artist, title):
    genius_url = search_song_on_genius(artist, title)
    if genius_url:
        return get_lyrics(genius_url)
    else:
        print("❌ Genius'ta şarkı bulunamadı.")
        return None
    
if __name__ == "__main__":
    artist = "The Weeknd"
    title = "Blinding Lights"
    lyrics = get_lyrics_by_search(artist, title)
    if lyrics:
        print("🎉 Sözler:")
        print(lyrics)
    else:
        print("❌ Lyrics alınamadı.")

    with open("blinding_lights_lyrics.txt", "w", encoding="utf-8") as f:
        f.write(lyrics)
    print("💾 Sözler dosyaya kaydedildi.")   