const scanWin = document.getElementById('scanWin');
let isDragging = false;
let dragTarget = null;
let offsetX = 0;
let offsetY = 0;

function setupDragEvents(elem) {
    elem.addEventListener('mousedown', function(e) {
      if (e.target.tagName.toLowerCase() === 'button') return; // 忽略点击关闭按钮
      isDragging = true;
      dragTarget = elem;
      offsetX = e.clientX - elem.offsetLeft;
      offsetY = e.clientY - elem.offsetTop;
      elem.style.cursor = 'grabbing';
    });
}
setupDragEvents(scanWin);

document.addEventListener('mousemove', function(e) {
    if (isDragging && dragTarget) {
      dragTarget.style.left = (e.clientX - offsetX) + 'px';
      dragTarget.style.top = (e.clientY - offsetY) + 'px';
    }
});

document.addEventListener('mouseup', function() {
    if (isDragging && dragTarget) {
      dragTarget.style.cursor = 'move';
    }
    isDragging = false;
    dragTarget = null;
});