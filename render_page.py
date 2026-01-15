from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from fid_interpretation import resolve_as_tree
import os
import time
# import mail
# THIS IS A TEMPORARY FILE FOR TEST !
# Later, this file will be merged into main.

app = Flask(__name__)
# @app.route('/', methods=['GET'])
# def index():
#     return render_template('main_page.html')
app.secret_key = 'test_environment'
# will be stored into /secrets

@app.route('/scanWindow', methods=['GET'])
def scan_window():
    return render_template('upload_file.html', emails=['mail1','mail2','mail3','mail4']) # mail.get_recent_mails(7)



@app.route('/file', methods=['POST'])
def post():
    # 检查请求中是否有文件
    # if 'file' not in request.files:
    #     return redirect('/label')
    #
    # file = request.files['file']
    #
    # # 确保文件类型是 JPG
    # if file and file.filename.endswith('.jpg'):
    #     # 生成文件名（当前时间戳 + .jpg）
    #     timestamp = time.time()
    #     filename = f"{timestamp}.jpg"
    #     file_path = os.path.join('temp', filename)
    #
    #     # 保存文件
    #     file.save(file_path)
    #
    #     # 将文件名存入 session
    #     session['filename'] = filename
    #
    #     # 重定向到 /label 页面
    #     return redirect('/label')
    session['filename'] = '1.jpg'
    return redirect('/label')
    # return 'Invalid file format', 400


@app.route('/label')
def label():
    # 获取文件名
    filename = session.get('filename', None)

    if filename:
        return f'File {filename} uploaded successfully!'
    else:
        return 'No file uploaded.', 400
# @app.route('/file', methods=['PUT'])
# def put():
#     return render_template('main_page.html', emails=["put got!"])

# @app.route('/file', methods=['DELETE'])
# def delete():
#     return render_template('main_page.html', emails=["delete got!"])

tree = resolve_as_tree()
def flatten_tree(node_tree):
    flat = {}
    def _flatten(node):
        flat[node['id']] = node
        for child in node.get('children', []):
            _flatten(child)
    for root in node_tree:
        _flatten(root)
    return flat

flat_map = flatten_tree(tree)

@app.route("/setting", methods=["GET"])
def setting():
    return render_template("settings.html", tree_data=tree)

@app.route("/api_setting", methods=["GET"])
def api_setting():
    return render_template("ai_api_set.html", tree_data=tree)

@app.route("/")
def index():
    return render_template("main_page.html")

@app.route("/node_info", methods=["POST"])
def node_info():
    data = request.get_json()
    node_id = data.get("id")
    node = flat_map.get(node_id)
    if node:
        return jsonify(node)
    return jsonify({"error": "节点不存在"}), 404

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=2333)