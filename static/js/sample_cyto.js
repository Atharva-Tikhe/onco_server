var script = document.getElementById("dynamicScript");

var recdAttr = script.getAttribute("data");

// console.log(`this is coming from sample cyto \n the selection is ${recdAttr}`);

$.getScript(`/networks/${recdAttr}`, function (data) {
  console.log(`serving ${recdAttr}`);
  $("#loading").hide();
});

