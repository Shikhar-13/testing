const hamBurger = document.querySelector(".toggle-btn");

hamBurger.addEventListener("click", function () {
    document.querySelector("#sidebar").classList.toggle("expand");
});


document.getElementById('search-input').addEventListener('click', function() {
  document.getElementById('search-result').classList.remove('d-none');
});
document.addEventListener('click', function(event) {
const searchInput = document.getElementById('search-input');
const searchResult = document.getElementById('search-result');

if (!searchInput.contains(event.target) && !searchResult.contains(event.target)) {
searchResult.classList.add('d-none');
}
});



$(".toggle-btn").click(function(){
$(".main").toggleClass("active");
$(".top-header").toggleClass("active");
});


$(window).on('load resize', function() {
  if ($(window).width() < 1181) {
      $("#sidebar").removeClass("expand");
      $(".main").addClass("active");
      $(".top-header").addClass("active");
  } else {
      // If the window width is 1024 pixels or more
      // you might want to reverse the actions
      $("#sidebar").addClass("expand");
      $(".main").removeClass("active");
  }
});

