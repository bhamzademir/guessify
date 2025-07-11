import subprocess
import random
import uuid
import requests
import os
import time

# FFmpeg binary yolları (senin miniconda içindeki ffmpeg konumu)
FFMPEG_PATH = "C:/Users/bedir/miniconda3/pkgs/ffmpeg-4.3-ha925a31_0/Library/bin/ffmpeg.exe"
FFPROBE_PATH = "C:/Users/bedir/miniconda3/pkgs/ffmpeg-4.3-ha925a31_0/Library/bin/ffprobe.exe"

def download_audio(url, output_path, retries=3):
    """
    Ses URL’sinden dosyayı indirir, bağlantı hatalarında tekrar dener.
    """
    print(f"⬇️ Ses indiriliyor: {url}")
    headers = {"User-Agent": "Mozilla/5.0"}

    for attempt in range(1, retries + 1):
        try:
            with requests.get(url, stream=True, timeout=15, headers=headers) as response:
                response.raise_for_status()
                with open(output_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
            print("✅ İndirme tamamlandı.")
            return output_path
        except Exception as e:
            print(f"⚠️ Deneme {attempt}/{retries} başarısız: {e}")
            time.sleep(2)

    raise Exception("❌ Ses indirilemedi, bağlantı sürekli kesiliyor.")

def crop_audio_with_ffmpeg(input_file, output_file, snippet_duration=10):
    result = subprocess.run(
        [FFPROBE_PATH, "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", input_file],
        capture_output=True, text=True
    )
    total_duration = float(result.stdout.strip())

    if snippet_duration >= total_duration:
        start_time = 0
    else:
        start_time = random.uniform(0, total_duration - snippet_duration)

    print(f"🔪 Kesit: {start_time:.2f}s → {start_time + snippet_duration:.2f}s")

    subprocess.run([
        FFMPEG_PATH, "-y", "-i", input_file,
        "-ss", str(round(start_time, 2)),
        "-t", str(snippet_duration),
        "-vn",
        "-c:a", "libmp3lame",
        "-b:a", "192k",
        output_file
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    return output_file


def generate_snippet_from_url(audio_url, duration=12, output_path=None):
    temp_raw = f"raw_{uuid.uuid4()}.mp4"
    temp_snippet = output_path or f"snippet_{uuid.uuid4()}.mp3"

    download_audio(audio_url, temp_raw)
    crop_audio_with_ffmpeg(temp_raw, temp_snippet, snippet_duration=duration)

    os.remove(temp_raw)
    return temp_snippet

