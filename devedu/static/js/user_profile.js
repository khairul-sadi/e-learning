const btn_learnings = document.querySelectorAll(".btn-learnings")
const btn_wishlist = document.querySelectorAll(".btn-wishlist")

const learning_container = document.querySelector(".my_learnings")
const wishlist_container = document.querySelector(".wishlist")

btn_learnings.forEach((btn) => {
    btn.addEventListener("click", () => {
        wishlist_container.classList.add("hidden")
        learning_container.classList.remove("hidden")
    })
})
btn_wishlist.forEach((btn) => {
    btn.addEventListener("click", () => {
        learning_container.classList.add("hidden")
        wishlist_container.classList.remove("hidden")
    })
})


// ! ------------- Rating Stars ---------------------
const ratings= document.querySelectorAll(".rating")

ratings.forEach((r) => {
    const rate_arr = r.querySelector(".course_rating").textContent.split(".")
    const stars = r.querySelectorAll(".avg-star")

    rate_arr[0] = parseInt(rate_arr[0])
    rate_arr[1] = parseInt(rate_arr[1])

    stars.forEach((star) => {
        star.classList.add("not-filled")
    });

    if (rate_arr[1] > 5) {
        rate_arr[0] += 1
        rate_arr[1] = 0
    }
    else if (rate_arr[1] > 0 && rate_arr[1] < 6) {
        rate_arr[1] = 5
    }

    if (rate_arr[1] == 5) {
        stars[rate_arr[0]].textContent = "star_half"
    }

    for (let i=0; i<rate_arr[0]; i++) {
        stars[i].classList.remove("not-filled")
    }

})
