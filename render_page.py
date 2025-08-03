from flask import Flask, render_template

app = Flask(__name__)
@app.route('/', methods=['GET'])
def index():
    return render_template('scan.html', emails=["test_email_content_one_a_b_c","test_email_content_two_a_b_c", "test_email_content_three_a_b_c", "test_email_content_four_a_b_c", "test_email_content_five_a_b_c"])

@app.route('/', methods=['POST'])
def post():
    return render_template('scan.html', emails=["post got!"])

@app.route('/', methods=['PUT'])
def put():
    return render_template('scan.html', emails=["put got!"])

@app.route('/', methods=['DELETE'])
def delete():
    return render_template('scan.html', emails=["delete got!"])


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=443)