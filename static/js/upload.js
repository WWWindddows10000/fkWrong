const dropZone = document.getElementById('upload'); // 定义在顶部，所有函数可访问

  function handleEmail(index) {
    // 在这里向flask后端以DELETE方式返回email编号
    fetch('/file', {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ emailIndex: index })
    })
    .then(response => {
    if (!response.ok) {
      return response.json().then(err => Promise.reject(new Error(err.message || `请求失败，状态码：${response.status}`)));
    }
    return response.json();
  })
    .then(response => response.json())
    .then(data => {
      if (data.redirect) {
        window.location.href = data.redirect;
      }
      dropZone.style.backgroundColor = 'aquamarine'; // 上传成功后恢复背景色
    })
    .catch(error => {
      console.error('上传失败:', error);
      alert('邮件失败: ' + error);
    });
  }
  function scan() {
    fetch('/file', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ "Gunmu" : "Diangun's mother" })    // 占位符，只要请求了就ok，因为这个是scan……
    })
  }

  dropZone.addEventListener('dragover', event => {
    event.stopPropagation();
    event.preventDefault();
    event.dataTransfer.dropEffect = 'copy';
    dropZone.style.backgroundColor = '#ef49ad'; // 改变背景色以示拖动
  });

  dropZone.addEventListener('dragleave', event => {
    dropZone.style.backgroundColor = 'aquamarine'; // 改变背景色以示拖动
  });

  dropZone.addEventListener('drop', event => {
    // Get the files
    const files = event.dataTransfer.files;
    //在这里向flask后端以put方式上传文件
    if (files.length > 0) {
      const formData = new FormData();
      formData.append('file', files[0]);
      fetch('/file', {
        method: 'PUT',
        body: formData
      })
      .then(response => response.json())
      .then(data => {
        if (data.redirect) {
          window.location.href = data.redirect;
        }
        dropZone.style.backgroundColor = 'aquamarine'; // 上传成功后恢复背景色
      })
      .catch(error => {
        console.error('上传失败:', error);
        alert('文件上传失败: ' + error);
        dropZone.style.backgroundColor = 'aquamarine';
      });
    }
    event.stopPropagation();
    event.preventDefault();
  });
