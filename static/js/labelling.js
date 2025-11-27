var canvas = document.getElementById("image");
var ctx = canvas.getContext("2d");  // 2D Drawing context
let isDrawing = false;
let startX, startY;

var img = new Image();
img.src = 'E:/Wei Qiuyue/fkwrong/static/picture/label-testpic.jpg';
img.onload = function() {
  ctx.drawImage(img, 10, 10, 100, 100);
}

canvas.addEventListener('mousedown', function(e) {
    isDrawing = true;
    startX = e.offsetX;
    startY = e.offsetY;
});


canvas.addEventListener('mouseup', function() {
    if (!isDrawing) return;
    isDrawing = false;
    let currentX = e.offsetX;
    let currentY = e.offsetY;
    ctx.strokeRect(startX, startY, currentX - startX, currentY - startY);  // Draw rectangle
});