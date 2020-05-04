import os
from flask import Flask, request, redirect, render_template, send_file
import web_check_availability
import web_online_trade_invoice
import web_ot_upd
import web_wb_deficit

UPLOAD_FOLDER = r'D:\Projects\WB scripts\files'
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
    out_of_stock = web_check_availability.check()
    return render_template('index.html', data=out_of_stock, count=len(out_of_stock))



@app.route('/ot_invoice/', methods=['POST'])
def ot_invoice():
    try:
        file_path = upload_file('ot_invoice_file')
        web_online_trade_invoice.make_ot_invoice(file_path)
        return send_file(file_path,
                         mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                         as_attachment=True)
    except KeyError:
        return "Возникла ошибка при обработке файла. Вероятные причины - не xlsx файл, в счете присутствуют наименования," \
               " отсутствующие в справочнике, файл отличается от формата в котором выгружается счет на оплату из 1С"


@app.route('/ot_upd/', methods=['POST'])
def ot_upd():
    file_path = upload_file('ot_upd_file')
    web_ot_upd.make_ot_upd(file_path, "OT", request.form['ot_invoice_num'])
    return send_file("D:\\Projects\\WB scripts\\output\\output.xml",
                     mimetype="application/xml",
                     as_attachment=True)


@app.route('/wb_upd/', methods=['POST'])
def wb_upd():
    file_path = upload_file('wb_upd_file')
    web_ot_upd.make_ot_upd(file_path, "WB", request.form['wb_invoice_num'])
    return send_file("D:\\Projects\\WB scripts\\output\\output.xml",
                     mimetype="application/xml",
                     as_attachment=True)


@app.route('/wb_stock/', methods=['POST'])
def wb_stock():
    file_path = upload_file('wb_stock')
    web_wb_deficit.make_file(file_path, request.form['file_type'])
    return send_file(file_path,
                     mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                     as_attachment=True)


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
