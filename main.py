# Main Program
"""
███████╗██╗  ██╗██╗    ██╗██████╗  ██████╗ ███╗   ██╗ ██████╗ 
██╔════╝██║ ██╔╝██║    ██║██╔══██╗██╔═══██╗████╗  ██║██╔════╝ 
█████╗  █████╔╝ ██║ █╗ ██║██████╔╝██║   ██║██╔██╗ ██║██║  ███╗
██╔══╝  ██╔═██╗ ██║███╗██║██╔══██╗██║   ██║██║╚██╗██║██║   ██║
██║     ██║  ██╗╚███╔███╔╝██║  ██║╚██████╔╝██║ ╚████║╚██████╔╝
╚═╝     ╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝                                                       
fkWrong! version 0.1.0 "Ampere"                                           
"""
import time
from rich.console import Console
import os
# from readSettings import resolveCode
import readSettings
from flask import Flask, render_template
from logMeth import log, l

app = Flask()
@app.route('/', methods=['GET'])
def index():
    return render_template('pages/index/index.html',rolling_message='欢迎您使用WinBookMan资料管理系统！版本号：{}。今天是：{}，祝您生活愉快！你在干什么‽'.format(version,datetime.now().strftime('%Y年%m月%d日')))

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=443)