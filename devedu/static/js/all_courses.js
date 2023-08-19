const review = document.querySelectorAll(".rating")

review.forEach((item) => {
    stars = item.querySelectorAll(".user-star")
    rating_arr = item.querySelector(".avr_rating").textContent.split(".")
    rating_arr[0] = parseInt(rating_arr[0])
    rating_arr[1] = parseInt(rating_arr[1])

    if(rating_arr[1] > 0 && rating_arr[1]<6){
        rating_arr[1] = 5;
    }
    else if (rating_arr[1] > 5) {
        rating_arr[0] += 1;
        rating_arr[1] = 0
    }

    stars.forEach((star) => {
        star.classList.add("not-filled")
    })

    for (let i=0; i < rating_arr[0]; i++) {
        stars[i].classList.remove("not-filled")
    }

    if(rating_arr[1] == 5) {
        stars[rating_arr[0]].textContent = "star_half"
    }
})



// ! ---------------------------------------------- Filters ---------------------------------------
// const test = document.getElementById("test")

// const sel_filter = document.getElementById("filter")
// const sel_sort = document.getElementById("sort")
// const btn_apply_filter = document.getElementById("apply_filter")
// const btn_clear_filter = document.getElementById("clear_filter")
// const query = document.querySelector(".searched_text").dataset.query;

// console.log(query)


// $(document).ready(function() {
//     $(btn_apply_filter).on("click", function() {
//         $.ajax({
//             type: "GET",
//             data: {
//                 query: query,
//                 sort: $(sel_sort).val(),
//                 filter: $(sel_filter).val(),
//             },
//             url: "{% url 'filter' %}",
//             success: function(response) {
//                 console.log(response)
//             },
//             error: function(response) {
//                 alert("Error")
//             }
//         });
//     });
// })