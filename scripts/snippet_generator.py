from youtube_search import get_best_audio_url_from_youtube
from audio_utils import generate_snippet_from_url

if __name__ == "__main__":
    query = "Blinding Lights The Weeknd"
    audio_url = get_best_audio_url_from_youtube(query)

    snippet_path = generate_snippet_from_url(audio_url, duration=12)
    print("✅ Snippet oluşturuldu:", snippet_path)
