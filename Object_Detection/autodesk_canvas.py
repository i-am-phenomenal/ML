from IPython.display import IFrame
import os 
js = """
    <input type="file" id="fileInput" multiple accept="image/*" style="display:none">
<a href="#" id="fileSelect">Select some files</a>
<div id="fileList">
    <p>No files selected!</p>
</div>

<script>
// Use the Image class exported from canvas library
var Image = canvasLib.Image;

var fileSelect = document.getElementById("fileSelect");
var fileInput = document.getElementById("fileInput");
var fileList = document.getElementById("fileList");
fileSelect.addEventListener("click", function (e) {
    if (fileInput) {
        fileInput.click();
    }
    e.preventDefault(); // prevent navigation to "#"
}, false);
fileInput.addEventListener("change", function (e) {
    var files = this.files;
    if (!files.length) {
        fileList.innerHTML = "<p>No files selected!</p>";
    } else {
        fileList.innerHTML = '';

        var list = document.createElement("ul");
        for (var i = 0; i < files.length; i++) {
            var file = files[i];

            var displayImage = (function (f) {
                return function (img) {
                    var li = document.createElement("li");
                    list.appendChild(li);
                    li.appendChild(img);

                    var info = document.createElement("span");
                    info.innerHTML = f.name + ": " + f.size + " bytes";
                    li.appendChild(info);
                };
            })(file);

            var img = new Image();
            img.loadFromFile(file, displayImage);
        }
        fileList.appendChild(list);
    }
});
</script>
"""

js1 = """
// Use the Canvas/Image class exported from canvas library
var Canvas = canvasLib.Canvas;
var Image = canvasLib.Image;

var Library = environment.library(canvasLibrary.id,canvasLibrary.version);
var url = Library.resourceURL("flower.jpg");
var img = new Image();
img.src = url;
img.onerror = function(e) {
    console.log("Can't load image: " + e);
};
img.onload = function() {
    // Create canvas
    var container= $("#canvasContainer");
    var canvas = new Canvas(container.width(), container.height())
    container.append(canvas);

    // Get the 2d rendering context to draw
    var ctx = canvas.getContext('2d');

    // Draw the image in the center
    var offsetX = (canvas.width - img.width ) / 2;
    var offsetY = (canvas.height - img.height ) / 2;
    ctx.translate(offsetX, offsetY);
    ctx.drawImage(img, 0, 0, img.width, img.height);

    // Draw a tilted text at (50, 100)
    ctx.font = '30px Impact';
    ctx.rotate(.1);
    ctx.fillText("Awesome!", 50, 100);

    // Draw the underline using path API
    var te = ctx.measureText('Awesome!');
    ctx.strokeStyle = 'rgba(0,0,0,0.5)';
    ctx.beginPath();
    ctx.lineTo(50, 102);
    ctx.lineTo(50 + te.width, 102);
    ctx.stroke();
};
"""
with open(os.getcwd() + "/output/autodesk1.html" , "w") as html:
    html.write(js)