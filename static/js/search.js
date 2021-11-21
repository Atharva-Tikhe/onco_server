var goBtn = document.querySelector(".go-btn");
var result = document.querySelector("#result");

goBtn.addEventListener("click", function fetchDisplay() {
  var cancer = $("#parent-dirs option:selected").val();

  const xhr = new XMLHttpRequest();

  xhr.open("GET", `http://127.0.0.1:5000/canceromics/${cancer}`, true);

  xhr.onload = function () {
    if (this.status === 200) {
      var headings = document.querySelectorAll("h3").forEach((element) => {
        element.innerHTML = "";
      });
      obj = JSON.parse(this.responseText);

      let parent = obj[`canceromics\\${cancer}`];

      for (let index = 0; index < parent.length; index++) {
        var h3 = document.createElement("h3");

        h3.textContent = parent[index];

        let files = obj[`canceromics\\${cancer}\\${parent[index]}`];

        console.log(files);
        if (files.length >= 1) {
          files.forEach((file) => {
            var anchor = document.createElement("a");
            anchor.innerHTML = file;
            anchor.setAttribute(
              "href",
              `canceromics/download/canceromics/${cancer}/${parent[index]}/${file}`
            );
            h3.appendChild(document.createElement("br"));
            h3.appendChild(anchor);
          });

          result.appendChild(h3);
        }
      }
    } else {
      console.log("File not found");
    }
  };
  xhr.send();
});
