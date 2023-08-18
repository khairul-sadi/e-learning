const video = document.querySelector("video");
const source = video.querySelector("source");
const contents = document.querySelectorAll(".content")

const pdf_reader = document.querySelector(".pdf-reader")

contents.forEach((c) => {
    const url = c.dataset.url
    const type = url.slice(-3)

    if (type == "mp4") {
        c.textContent = c.textContent + " (video)"
    }
    else if (type == "pdf") {
        c.textContent = c.textContent + " (pdf)"
    }

    c.addEventListener("click", () => {
        if (type == "mp4") {
            source.src = url;
            video.currentTime = 0
            video.muted = false;
            video.play();
        }
        else {
            pdf_reader.href = url;
            pdf_reader.click();
        }
    })
    console.log(type)
    console.log(url)
})


// ! -------------------------- Course Type ----------------------------
