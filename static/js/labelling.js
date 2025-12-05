const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const fillColor = ["rgba(205,92,92,0.6)","rgba(255,140,0,0.6)","rgba(238,232,170,0.6)",
                           "rgba(107,142,35,0.6)","rgba(34,139,34,0.6)","rgba(102,205,170,0.6)",
                           "rgba(0,139,139,0.6)","rgba(70,130,180,0.6)","rgba(135,206,250,0.6)","rgba(72,61,139,0.6)"];
const strokeColor = ["#CD5C5C", "#FF8C00", "#EEE8AA", "#6B8E23", "#228B22",
                             "#66CDAA", "#008B8B", "#4682B4", "#87CEFA", "#483D8B"];
const boxTextInput = document.getElementById('boxText');
let startX, startY, isDrawing = false, currentBoxNo = 1;
let boxes = [];
let nowBoxNo = 0;

const img = new Image();
img.src = '../static/picture/test_label.jpg';
img.onload = function() {
    ctx.drawImage(img, 10, 10);
}

function drawRect(x, y, width, height, colorNo, text) {
    ctx.beginPath();
    ctx.rect(x, y, width, height);
    ctx.lineWidth = 2;
    ctx.strokeStyle = strokeColor[colorNo];
    ctx.stroke();
    if (text != null) {
            ctx.fillStyle = 'black';
            ctx.font = '12px 宋体';
            ctx.fillText(text, x + 5, y + 15);
    }
}

function redrawAll() {
    ctx.drawImage(img, 10, 10);
    boxes.forEach(box => {
        ctx.fillStyle = fillColor[(box.boxNo - 1) % 10];
        ctx.fillRect(box.startX, box.startY, box.endX - box.startX, box.endY - box.startY);

        const borderColorNo = (box.boxNo - 1) % 10;
        drawRect(box.startX, box.startY, box.endX - box.startX, box.endY - box.startY, borderColorNo);

        ctx.fillStyle = 'black';
        ctx.font = '12px 宋体';
        ctx.fillText(box.text, box.startX + 5, box.startY + 15);
    });
}

// function createTextArea(box){
//     let miniForm = document.createElement('form-item');
// }

canvas.addEventListener('mousedown', function (e) {
    startX = e.offsetX;
    startY = e.offsetY;
    isDrawing = true;
});

canvas.addEventListener('mousemove', function (e) {
    if (isDrawing) {
        const width = e.offsetX - startX;
        const height = e.offsetY - startY;
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        redrawAll();
        const borderColorNo = nowBoxNo % 10;
        drawRect(startX, startY, width, height, borderColorNo, "绘制中");
    }
});


canvas.addEventListener('mouseup', function (e) {
    if (isDrawing) {
        const endX = e.offsetX;
        const endY = e.offsetY;
        const text = '无描述';
        boxes.push({
            boxNo: currentBoxNo++,
            startX: startX,
            startY: startY,
            endX: endX,
            endY: endY,
            text: text,
        });

        nowBoxNo++;
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        redrawAll();

        isDrawing = false;
    }
    console.log(boxes);
});

function clearCanvas() {
    boxes = [];
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}

// function submitText(currentBoxNo) {
//         let box = boxes[currentBoxNo]
//     const text = box.inputElement.value.trim();
//     if (text) {
//         box.text = text;
//     }
//     box.inputElement.style.display = 'none';
//     redrawAll();
// }


function submitData() {
        fetch('/submit_data', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
        body: JSON.stringify({ boxes: boxes }),
    })
    .then(response => response.json())
    .then(data => alert('数据提交成功！'))
    .catch(error => console.error('提交失败:', error));
}
