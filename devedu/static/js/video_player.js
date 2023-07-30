const videoBtn = document.querySelector(".video-btn");
const playerContainer = document.querySelector(".player__container");
const overlay = document.querySelector(".overlay");

videoBtn.addEventListener("click", () => {
  video.src = videoBtn.dataset.url;
  video.play();
  playerContainer.classList.remove("hidden");
  overlay.classList.remove("hidden");
});

overlay.addEventListener("click", () => {
  video.src = "";
  playerContainer.classList.add("hidden");
  overlay.classList.add("hidden");
});


// ! Getting our elements
const player = document.querySelector(".player");
const video = player.querySelector(".viewer");
const progress = player.querySelector(".progress");
const progressBar = player.querySelector(".progress__filled");
const toggle = player.querySelector(".toggle");
const skipButtons = player.querySelectorAll("[data-skip]");
const ranges = player.querySelectorAll("player__slider");

const screenSizeBtn = player.querySelector(".screen__size");

// ! Build Functions
function togglePlay() {
  if (video.paused) {
    video.play();
  } else {
    video.pause();
  }
}

function updateButton() {
  const icon = this.paused ? "►" : "  ❚❚";
  toggle.textContent = icon;
}

function skip() {
    video.addEventListener('loadedmetadata', function() {
        console.log("Video loaded")
        video.currentTime += parseFloat(this.dataset.skip);
    })
}

function handleRangeUpdate() {
  video[this.name] = this.value;
}

function handleProgress() {
  const percent = (video.currentTime / video.duration) * 100;
  progressBar.style.flexBasis = `${percent}%`;
}

function scrub(e) {
    // video.addEventListener('loadedmetadata', function() {
        const scrubTime = (e.offsetX / progress.offsetWidth) * video.duration;
        video.currentTime = scrubTime;
    // })
}

function screenSize() {
  if (screenSizeBtn.dataset.size == 1) {
    video.requestFullscreen();
  }
}

// ! Hookup the event listeners
video.addEventListener("click", togglePlay);
video.addEventListener("play", updateButton);
video.addEventListener("pause", updateButton);
video.addEventListener("timeupdate", handleProgress);

toggle.addEventListener("click", togglePlay);

skipButtons.forEach((button) => button.addEventListener("click", skip));

ranges.forEach((range) => addEventListener("change", handleRangeUpdate));

let mousedown = false;
progress.addEventListener("click", scrub);
progress.addEventListener("mousemove", (e) => mousedown && scrub(e));
progress.addEventListener("mousedown", () => (mousedown = true));
progress.addEventListener("mouseup", () => (mousedown = false));



// ? Custom

screenSizeBtn.addEventListener("click", screenSize);

document.addEventListener("keydown", (e) => {
  const name = e.key;
  const code = e.code;
  if (code == "Space") {
    if (video.paused) {
      video.play();
    } else {
      video.pause();
    }
  } else if (code == "KeyF") {
    if (window.innerHeight == screen.height) {
      document.exitFullscreen();
    } else {
      video.requestFullscreen();
    }
  }
});


// const videoBtn = document.querySelector(".video-btn");
// const playerContainer = document.querySelector(".player__container");
// const overlay = document.querySelector(".overlay");

// videoBtn.addEventListener("click", () => {
//   video.src = videoBtn.dataset.url;
//   video.play();
//   playerContainer.classList.remove("hidden");
//   overlay.classList.remove("hidden");
// });

// overlay.addEventListener("click", () => {
//   video.src = "";
//   playerContainer.classList.add("hidden");
//   overlay.classList.add("hidden");
// });
