import os
from flask import Flask, request, redirect, render_template, send_file
import check_availability
import web_online_trade_invoice
import web_ot_upd

UPLOAD_FOLDER = r'D:\Projects\WB scripts\web\files'
ALLOWED_EXTENSIONS = {'xlsx'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/upload/', methods=['POST'])
def upload_file(name):
    file = request.files[name]
    if file and allowed_file(file.filename):
        basedir = os.path.abspath(os.path.dirname(__file__))
        filename = file.filename
        file_path = os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        file.close()
    else:
        file_path = None
    redirect("/")
    return file_path


@app.route('/check_av/', methods=['GET', 'POST'])
def check_av():
    out_of_stock = check_availability.check_availability()
    return render_template('index.html', data=out_of_stock)


@app.route('/ot_invoice/', methods=['POST'])
def ot_invoice():
    file_path = upload_file('ot_invoice_file')
    web_online_trade_invoice.make_ot_invoice(file_path)
    return send_file(file_path,
                     mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                     as_attachment=True)


@app.route('/ot_upd/', methods=['POST'])
def ot_upd():
    file_path = upload_file('ot_upd_file')
    web_ot_upd.make_ot_upd(file_path)
    return send_file(file_path,
                     mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                     as_attachment=True)


@app.route('/wb_xml_from_invoice/', methods=['POST'])
def wb_xml_from_invoice():
    return "wb_xml_from_invoice"


@app.route('/wb_stock/', methods=['POST'])
def wb_stock():
    return "wb_stock"


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
