from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/check_availability/', methods=['POST'])
def check_availability():
    return "check_availability"


@app.route('/online_trade_invoice/', methods=['POST'])
def online_trade_invoice():
    return


@app.route('/wb_xml_from_invoice/', methods=['POST'])
def wb_xml_from_invoice():
    return "wb_xml_from_invoice"


@app.route('/wb_stock/', methods=['POST'])
def wb_stock():
    return "wb_stock"


if __name__ == '__main__':
    app.run(debug=True)
