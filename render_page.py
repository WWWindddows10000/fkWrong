from flask import Flask, render_template
from readSettings import resolveAsTree
from flask import request, jsonify


app = Flask(__name__)
# @app.route('/', methods=['GET'])
# def index():
#     return render_template('scan.html')

@app.route('/scanWindow', methods=['GET'])
def scan_window():
    return render_template('scan copy.html', emails=["scanwindow","test_email_content_two_a_b_c", "test_email_content_three_a_b_c_test_for_marquee_brackets", "test_email_content_four_a_b_c", "test_email_content_five_a_b_c"])

# @app.route('/', methods=['POST'])
# def post():
#     return render_template('scan.html', emails=["post got!"])

# @app.route('/', methods=['PUT'])
# def put():
#     return render_template('scan.html', emails=["put got!"])

# @app.route('/', methods=['DELETE'])
# def delete():
#     return render_template('scan.html', emails=["delete got!"])

tree = resolveAsTree()
print(tree)
# 将平铺 id->node 映射
def flatten_tree(tree):
    flat = {}
    def _flatten(node):
        flat[node['id']] = node
        for child in node.get('children', []):
            _flatten(child)
    for root in tree:
        _flatten(root)
    return flat

flat_map = flatten_tree(tree)

@app.route("/setting", methods=["GET"])
def setting():
    return render_template("settings.html", tree_data=tree)

@app.route("/")
def index():
    return render_template("scan.html")

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