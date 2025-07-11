let currentQuery = ""; // Sunucudan gelen gerçek şarkı adı (gizli tutulacak)

console.log("✅ script.js loaded");

function fetchSnippet() {
  fetch("http://localhost:8000/api/snippet")
    .then(res => res.json())
    .then(data => {
      const audio = document.getElementById("audio-player");
      const lyricsDiv = document.getElementById("lyrics");

      if (data.snippet_url) {
        audio.src = "http://localhost:8000" + data.snippet_url;
        audio.play();
        currentQuery = data.query;  // Sunucudan gelen şarkı adı
        lyricsDiv.textContent = data.lyrics; // Lyrics'i göster
      }
    })
    .catch(err => {
      console.error("❌ Snippet yükleme hatası:", err);
    });
}

function submitGuess() {
  const userGuess = document.getElementById("guess-input").value.trim();
  const resultText = document.getElementById("result-text");

  if (!userGuess) {
    resultText.textContent = "Lütfen bir tahmin gir.";
    return;
  }

  fetch("http://localhost:8000/api/check", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      guess: userGuess,
      answer: currentQuery
    })
  })
    .then(res => res.json())
    .then(data => {
      if (data.correct) {
        resultText.textContent = "✅ Doğru tahmin!";
      } else {
        resultText.textContent = "❌ Yanlış. Tekrar dene!";
      }
    })
    .catch(err => {
      console.error("❌ Tahmin kontrol hatası:", err);
      resultText.textContent = "Hata oluştu.";
    });
}

// Sayfa yüklendiğinde ilk snippet gelsin
window.addEventListener("DOMContentLoaded", () => {
  console.log("🎶 Sayfa yüklendi, snippet çekiliyor...");
  fetchSnippet();
});
