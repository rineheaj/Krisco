let player;
let playerReady = false;

function onYouTubeIframeAPIReady() {
  player = new YT.Player("bg-music", {
    events: {
      onReady: () => {
        playerReady = true;
      }
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  const playBtn = document.getElementById("playBtn");
  const pauseBtn = document.getElementById("pauseBtn");
  const resetBtn = document.getElementById("resetBtn");
  const muteBtn = document.getElementById("muteBtn");
  const placeholder = document.getElementById("videoPlaceholder");

  // Start / Play
  playBtn.addEventListener("click", () => {
    if (!playerReady) return;
    player.playVideo();
    placeholder.textContent = "🎵 Now Playing";
    placeholder.classList.add("playing")
  });

  // Pause
  pauseBtn.addEventListener("click", () => {
    if (!playerReady) return;
    player.pauseVideo();
    placeholder.textContent = "⏸ Paused";
    placeholder.classList.remove("playing")
  });

  // Reset
  resetBtn.addEventListener("click", () => {
    if (!playerReady) return;
    player.stopVideo();
    placeholder.textContent = "🎵 Music is ready";
    placeholder.classList.remove("playing")
  });

  // Mute / Unmute
  muteBtn.addEventListener("click", () => {
    if (!playerReady) return;
    if (player.isMuted()) {
      player.unMute();
      muteBtn.textContent = "🔊";
    } else {
      player.mute();
      muteBtn.textContent = "🔇";
    }
  });
});
