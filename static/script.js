let player;
let hasOptedIn = localStorage.getItem("musicPlaying") === "true";
let isMuted = localStorage.getItem("musicMuted") === "true";
let savedTime = parseFloat(localStorage.getItem("musicTime")) || 0;

function onYouTubeIframeAPIReady() {
  player = new YT.Player("bg-music", {
    events: {
      onReady: (event) => {
        if (player.isMuted()) {
          isMuted = true;
          localStorage.setItem("musicMuted", "true");
          document.getElementById("muteBtn").textContent = "🔇 Muted";
        }
          else {
            isMuted = false;
            localStorage.setItem("musicMuted", "false");
            document.getElementById("muteBtn").textContent = "🔊 Unmuted";
          }
        

        if (hasOptedIn) {
          if (savedTime > 0) {
            event.target.seekTo(savedTime, true);
          }
          if (isMuted) {
            event.target.mute();
          }
          event.target.playVideo();
        }


        setInterval(() => {
          if (hasOptedIn) {
            localStorage.setItem("musicTime", player.getCurrentTime());
          }
        }, 2000);
      }
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  const playBtn = document.getElementById("playBtn");
  const muteBtn = document.getElementById("muteBtn");
  const placeholder = document.getElementById("videoPlaceholder");

  // --- Initial UI state ---
  if (hasOptedIn) {
    playBtn.textContent = "🎵 Music Playing";
    playBtn.disabled = true;
    placeholder.textContent = "🎵 Now Playing";
    placeholder.classList.add("playing");
  } else {
    playBtn.textContent = "▶️ Play Music";
    playBtn.disabled = false;
    placeholder.textContent = "🎵 Music is ready to play";
    placeholder.classList.remove("playing");
  }
  muteBtn.textContent = isMuted ? "🔇 Muted" : "🔊 Unmuted";

  // --- Play button ---
  playBtn.addEventListener("click", () => {
    player.playVideo();
    playBtn.textContent = "🎵 Music Playing";
    playBtn.disabled = true;
    placeholder.textContent = "🎵 Now Playing";
    placeholder.classList.add("playing");

    // Mark that the user has opted in
    hasOptedIn = true;
    localStorage.setItem("musicPlaying", "true");
  });

  // --- Mute button ---
  muteBtn.addEventListener("click", () => {
    if (player.isMuted()) {
      player.unMute();
      isMuted = false;
    } else {
      player.mute();
      isMuted = true;
    }
    localStorage.setItem("musicMuted", isMuted);
    muteBtn.textContent = isMuted ? "🔇 Muted" : "🔊 Unmuted";
  });
});
