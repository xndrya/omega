import os
from flask import Flask, flash, request, redirect, url_for, render_template, send_file
import check_availability
import web_online_trade_invoice

UPLOAD_FOLDER = r'D:\Projects\WB scripts\web\files'
ALLOWED_EXTENSIONS = {'xlsx'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            basedir = os.path.abspath(os.path.dirname(__file__))
            # filename = secure_filename(file.filename)
            filename = file.filename
            file.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))
            file.close()
            web_online_trade_invoice.make_ot_invoice(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))
            return send_file(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename),
                             mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                             as_attachment=True)
            # return redirect("/")

    return '''
    <!doctype html>
    <title>Загрузка файла</title>
    <h1>Загрузка файла</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file required>
      <input type=submit value=Upload>
    </form>
    '''


@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/check_av/', methods=['GET', 'POST'])
def check_av():
    out_of_stock = check_availability.check_availability()
    return render_template('index.html', data=out_of_stock)


@app.route('/ot_invoice/', methods=['POST'])
def ot_invoice():
    file = upload_file()
    # online_trade_invoice.make_ot_invoice(file)
    return f"{file}"


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
