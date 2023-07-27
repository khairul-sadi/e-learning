const btn_apply = document.querySelector(".btn-apply")
const btn_apply_no = document.querySelector(".btn-apply-no")
const terms = document.querySelector(".terms")
const overlay = document.querySelector(".overlay")

// window.addEventListener("DOMContentLoaded", () => {
    btn_apply.addEventListener("click", ()=> {
        terms.classList.remove("hidden")
    })

// })


overlay.addEventListener("click", () => {
    terms.classList.add("hidden")
})

btn_apply_no.addEventListener("click", () => {
    terms.classList.add("hidden")
})