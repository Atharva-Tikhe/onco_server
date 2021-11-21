$(document).ready(function () {
  $("#loading").hide();
});

const btn = document.getElementById("submit");

btn.addEventListener("click", function () {
  $("#viz").css("display", "block");

  $("#cy").empty();

  console.log("btn clicked!");
  var selectedValueCancer = $("#cancer-type").find(":selected").val();

  var selectedTypeViz = $("#viz-type").find(":selected").val();

  var fetchThis = selectedTypeViz + "/" + selectedValueCancer;

  let scriptTag = document.getElementById("dynamicScript");

  if (scriptTag === null) {
    let myScript = document.createElement("script");
    myScript.setAttribute("id", "dynamicScript");
    myScript.setAttribute("src", "/static/js/sample_cyto.js");
    myScript.setAttribute("data", fetchThis);
    console.log(`fetching ${fetchThis}`);
    document.body.appendChild(myScript);
  } else {
  }
});
