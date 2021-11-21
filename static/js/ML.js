var formContainer = document.getElementById("form-container");
var container = document.getElementById("container");
var form = document.querySelector("form");
var button = document.getElementById("submit-btn");
var file = document.getElementById("formFile");
var loading = document.getElementById("status");

button.addEventListener("click", function (event) {
  // event.preventDefault();

  console.log(loading.childElementCount);

  if (loading.childElementCount < 1) {
    var text = document.createElement("h6");
    text.innerText = "Running ML job... This may take some time.";
    var spinner = document.createElement("div");
    spinner.classList.add("spinner-grow");
    loading.appendChild(text);
    loading.appendChild(spinner);
  }
});

file.addEventListener("change", () => {
  // Get our CSV file from upload
  var file = document.getElementById("formFile").files[0];

  // Instantiate a new FileReader
  var reader = new FileReader();

  // Read our file to an ArrayBuffer
  reader.readAsArrayBuffer(file);

  // Handler for onloadend event.  Triggered each time the reading operation is completed (success or failure)
  reader.onloadend = function (evt) {
    // Get the Array Buffer
    var data = evt.target.result;

    // Grab our byte length
    var byteLength = data.byteLength;

    // Convert to conventional array, so we can iterate though it
    var ui8a = new Uint8Array(data, 0);

    // Used to store each character that makes up CSV header
    var headerString = "";

    // Iterate through each character in our Array
    for (var i = 0; i < byteLength; i++) {
      // Get the character for the current iteration
      var char = String.fromCharCode(ui8a[i]);

      // Check if the char is a new line
      if (char.match(/[^\r\n]+/g) !== null) {
        // Not a new line so lets append it to our header string and keep processing
        headerString += char;
      } else {
        // We found a new line character, stop processing
        break;
      }
    }

    var headerArray = headerString.split(",");

    var radioButtonContainer = document.querySelector(".header-btn-group");

    document.getElementById("target-col-label").classList.remove("invisible");
    document.getElementById("ml-method-label").classList.remove("invisible");
    document.getElementById("ml-method").classList.remove("invisible");
    document.getElementById("submit-btn").classList.remove("invisible");

    headerArray.forEach((element) => {
      var input = document.createElement("input");
      input.type = "radio";
      input.classList.add("btn-check");
      input.classList.add("m-3");
      input.name = "radio-part";
      input.value = `${element}`;
      input.id = `${element}-radio`;
      input.autocomplete = "off";

      if (headerArray.indexOf(element) == 0) {
        input.checked = true;
      }

      var label = document.createElement("label");
      label.classList.add("btn");
      label.classList.add("btn-outline-primary");
      label.classList.add("mx-3");
      label.htmlFor = input.id;
      label.innerHTML = element;

      radioButtonContainer.appendChild(input);
      radioButtonContainer.appendChild(label);
    });

    console.log(headerArray);
  };
});
