let currentQuery = ""; // Sunucudan gelen gerçek şarkı adı (gizli tutulacak)
let playerName = "";

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
      player: playerName,
      guess: userGuess
    })
  })
    .then(res => res.json())
    .then(data => {
      if (data.correct) {
        if (data.winner) {
          resultText.textContent = `✅ Doğru! ${data.winner} kazandı!`;
          fetchSnippet();
        } else {
          resultText.textContent = "✅ Doğru!";
        }
      } else {
        resultText.textContent = "❌ Yanlış. Tekrar dene!";
      }
      updateScoreboard(data.scoreboard);
    })
    .catch(err => {
      console.error("❌ Tahmin kontrol hatası:", err);
      resultText.textContent = "Hata oluştu.";
    });
}

function updateScoreboard(scores) {
  const scoresDiv = document.getElementById("scores");
  scoresDiv.innerHTML = "";
  for (const player in scores) {
    const p = document.createElement("p");
    p.textContent = `${player}: ${scores[player]}`;
    scoresDiv.appendChild(p);
  }
}

// Sayfa yüklendiğinde oyuncu adı istenip snippet gelsin
window.addEventListener("DOMContentLoaded", () => {
  playerName = prompt("Adınızı girin:") || `Player-${Math.floor(Math.random()*1000)}`;
  const infoDiv = document.getElementById("player-info");
  infoDiv.textContent = `Oyuncu: ${playerName}`;
  fetchSnippet();
});
