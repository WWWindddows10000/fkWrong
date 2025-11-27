window.onload = function(){
    window.addEventListener('message',function(e){
        console.log(e.data)
    })
}
document.getElementById('scanButton').onclick = function() {
  document.getElementById('scanWin').style.display = 'block';
};
document.getElementById('closeScanWin').onclick = function() {
  document.getElementById('scanWin').style.display = 'none';
};
document.getElementById('settingsButton').onclick = function() {
  document.getElementById('main_ui').innerHTML = `<iframe
    id="settingsWindow"
    title="设置"
    width="804"
    height="500"
    src="/setting">
  </iframe>`;
  document.getElementById('toolBar').innerHTML = `
  <ui>
  <li id="node" onClick="node()">节点设置</li>
  <li id="api" onClick="api()">AI API设置</li></ui>
  `;
};
function api(){
    document.getElementById('main_ui').innerHTML = `<iframe
        id="settingsWindow"
        title="设置"
        width="804"
        height="500"
        src="/api_setting">
        </iframe>`;
}
function node(){
    document.getElementById('main_ui').innerHTML = `<iframe
        id="settingsWindow"
        title="设置"
        width="804"
        height="500"
        src="/setting">
        </iframe>`;
}