from flask import Flask, render_template, request, jsonify
from read_settings import resolve_as_tree
import mail

app = Flask(__name__)
# @app.route('/', methods=['GET'])
# def index():
#     return render_template('main_page.html')

@app.route('/scanWindow', methods=['GET'])
def scan_window():
    return render_template('upload_file.html', emails=mail.get_recent_mails(7))


# @app.route('/', methods=['POST'])
# def post():
#     return render_template('main_page.html', emails=["post got!"])

# @app.route('/', methods=['PUT'])
# def put():
#     return render_template('main_page.html', emails=["put got!"])

# @app.route('/', methods=['DELETE'])
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
    app.run(debug=True, host='localhost', port=443)