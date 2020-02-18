# app.py

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect, url_for, flash
from flask import send_from_directory
from models import Schema, Book
from werkzeug.utils import secure_filename
import os
import random
import string

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
    return render_template('home.html', books=B.all())


@app.route('/upload/', methods=['GET', 'POST'])
def upload():
    errorMessage = 'Please submit a valid file'
    successMessage = 'File uploaded succesfully'

    if request.method == 'POST':
        # Check for file existance
        if 'file' not in request.files:
            flash(errorMessage)
            return redirect(url_for('upload'))

        # Check for file consistency
        file = request.files['file']
        if file.filename == '':
            flash(errorMessage)
            return redirect(url_for('upload'))

        # Check for file extension
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            # Get valid username if submitted
            username = request.form.get('username', None)
            if username == '':
                username = None

            # Build filename with random component
            filenameSplitted = filename.rsplit('.', 1)
            filename = '.'.join([
                filenameSplitted[0],
                ''.join(random.choices(string.ascii_letters, k=8)),
                filenameSplitted[1]
            ])

            # Save file in storage folder
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # Save file into the database
            b = Book()
            b.create(filename, str(request.remote_addr), username)

            # Notify
            flash(successMessage)
            return redirect(url_for('upload'))

    return render_template('upload.html')


@app.route('/book/<int:_id>')
def bookPage(_id):
    b = Book()
    return render_template('book.html', book=b.select(_id))


@app.route('/book/<int:_id>/download')
def bookDownload(_id):
    b = Book()
    book = b.select(_id)
    if book:
        return send_from_directory(app.config['UPLOAD_FOLDER'], book['name'])

    return redirect(url_for('home'))


if __name__ == '__main__':
    Schema()
    app.run(debug=True)
