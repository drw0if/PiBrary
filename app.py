# app.py

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect, url_for, flash
from models import Schema, Book
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

"""
get config
"""
app.config['UPLOAD_FOLDER'] = 'storage/'
app.secret_key = 'asd'
ALLOWED_EXTENSIONS = {'pdf', 'epub'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    B = Book()
    return render_template('home.html', books=B.select())


@app.route('/upload/', methods=['GET', 'POST'])
def upload():
    errorMessage = 'Please submit a valid file'
    successMessage = 'File uploaded succesfully'

    if request.method == 'POST':
        if 'file' not in request.files:
            flash(errorMessage)
            return redirect(url_for('upload'))

        file = request.files['file']
        if file.filename == '':
            flash(errorMessage)
            return redirect(url_for('upload'))

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash(successMessage)
            return redirect(url_for('upload'))

    return render_template('upload.html')


if __name__ == '__main__':
    Schema()
    app.run(debug=True)
