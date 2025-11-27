var canvas = document.getElementById("image");
var ctx = canvas.getContext("2d");  // 2D Drawing context
let isDrawing = false;
let startX, startY;
let boxes = [];  // 存储框的位置和尺寸

canvas.addEventListener('mousedown', function(e) {
    isDrawing = true;
    startX = e.offsetX;
    startY = e.offsetY;
});

canvas.addEventListener('mousemove', function(e) {
    if (!isDrawing) return;

    // 保持之前的框不被清除
    let currentX = e.offsetX;
    let currentY = e.offsetY;

    // 在绘制时不清除画布，直接绘制当前框
    ctx.clearRect(0, 0, canvas.width, canvas.height);  // 清空当前框区域
    drawAllBoxes();  // 重新绘制已经有的框

    // 绘制当前框
    ctx.strokeRect(startX, startY, currentX - startX, currentY - startY);
});

canvas.addEventListener('mouseup', function() {
    isDrawing = false;
    // 将框保存到数组
    boxes.push({ x: startX, y: startY, w: e.offsetX - startX, h: e.offsetY - startY, color: "blue" });
});

// 绘制所有框的函数
function drawAllBoxes() {
    boxes.forEach(function(box) {
        ctx.strokeStyle = box.color;
        ctx.strokeRect(box.x, box.y, box.w, box.h);
    });
}

var img = new Image();
img.src = 'E:/Wei Qiuyue/fkwrong/static/picture/label-testpic.jpg';
img.onload = function() {
  ctx.drawImage(img, 10, 10, 100, 100);
}


