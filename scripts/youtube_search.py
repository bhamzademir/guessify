import requests

def get_best_audio_url_from_youtube(query):
    """
    Arama terimi ile YouTube'dan en iyi ses kalitesine sahip stream URL'sini döner.
    """
    print(f"🔍 YouTube'da aranıyor: {query}")

    headers = {
        'user-agent': 'Mozilla/5.0',
        'content-type': 'application/json',
        'accept-language': 'en-GB,en;q=0.9',
    }

    json_data = {
        'query': query,
        'context': {
            'client': {
                'clientName': 'WEB',
                'clientVersion': '2.20250528.01.00',
            }
        },
        'params': '8AEB',  # reel videoları gösterebilir
    }

    # YouTube arama sonuçları
    res = requests.post(
        'https://www.youtube.com/youtubei/v1/search?prettyPrint=false',
        headers=headers,
        json=json_data
    )
    results = res.json().get('contents', {}) \
        .get('twoColumnSearchResultsRenderer', {}) \
        .get('primaryContents', {}) \
        .get('sectionListRenderer', {}) \
        .get('contents', [])[0] \
        .get('itemSectionRenderer', {}) \
        .get('contents', [])

    video_id = None
    for result in results:
        if 'videoRenderer' in result:
            video_id = result['videoRenderer'].get('videoId', None)
            break

    if not video_id:
        raise Exception("❌ Video ID bulunamadı.")

    # Player içeriği
    res2 = requests.post(
        f'https://youtubei.googleapis.com/youtubei/v1/player?id={video_id}&prettyPrint=false',
        headers={
            'user-agent': 'com.google.android.youtube/19.28.35',
            'x-goog-api-format-version': '2',
            'content-type': 'application/json',
        },
        json={
            'context': {
                'client': {
                    'clientName': 'ANDROID',
                    'clientVersion': '19.28.35',
                    'platform': 'MOBILE',
                }
            },
            'videoId': video_id,
        }
    )

    adaptive_formats = res2.json().get('streamingData', {}).get('adaptiveFormats', [])
    audio_qualities = ["AUDIO_QUALITY_UNKNOWN", "AUDIO_QUALITY_ULTRALOW", "AUDIO_QUALITY_LOW", "AUDIO_QUALITY_MEDIUM", "AUDIO_QUALITY_HIGH"]

    best_audio_url = ""
    best_quality_index = 0

    for fmt in adaptive_formats:
        if fmt.get('mimeType', '').startswith('audio/'):
            quality = fmt.get('audioQuality', 'AUDIO_QUALITY_UNKNOWN')
            index = audio_qualities.index(quality) if quality in audio_qualities else 0
            if index > best_quality_index:
                best_quality_index = index
                best_audio_url = fmt.get('url', '')

    if not best_audio_url:
        raise Exception("❌ Uygun ses URL'si bulunamadı.")

    print(f"✅ Seçilen ses kalitesi: {audio_qualities[best_quality_index]}")
    return best_audio_url
