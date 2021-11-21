var cancerType = document.getElementById("cancer-type-select");
var visualization = document.getElementById("visual");
var button = document.getElementById("submit");

button.addEventListener("click", function () {
  // alert("error in the script");
  if (visualization.options[visualization.selectedIndex].value == "Gene-Drug") {
    window.location.assign(
      `/cytoscape/network/${
        cancerType.options[cancerType.selectedIndex].value
      }/index.html`
    );
  }
  if (
    visualization.options[visualization.selectedIndex].value ==
    "Protein-Protein"
  ) {
    window.location.assign(
      `/cytoscape/network/prot-prot/${
        cancerType.options[cancerType.selectedIndex].value
      }/index.html`
    );
  }
});
