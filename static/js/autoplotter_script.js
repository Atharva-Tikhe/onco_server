var btn = document.querySelector("#backlink");

btn.addEventListener("click", function () {
  $.ajax("/eda/killall");
});
