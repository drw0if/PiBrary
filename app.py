# app.py

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect, url_for, flash
from flask import send_from_directory
from flask import abort
from models import Schema, Book, Vote
from werkzeug.utils import secure_filename
import os
import random
import string
from config import Config

app = Flask(__name__)

"""
get config
"""

config = Config().getConfiguration()

"""
set config
"""

app.config['UPLOAD_FOLDER'] = config['storageFolder']
app.secret_key = config['secretKey']
ALLOWED_EXTENSIONS = config['extensions']
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024  # 16MB


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def list():
    B = Book()
    return render_template('list.html', books=B.all())


@app.route('/upload/', methods=['GET', 'POST'])
def upload():
    errorMessage = 'Please submit a valid file'
    successMessage = 'File uploaded succesfully'

    if request.method == 'POST':
        # Check for file existance
        if 'file' not in request.files:
            flash(errorMessage, 'error')
            return redirect(url_for('upload'))

        # Check for file consistency
        file = request.files['file']
        if file.filename == '':
            flash(errorMessage, 'error')
            return redirect(url_for('upload'))

        # Check for file extension
        if file:
            if not allowed_file(file.filename):
                flash(errorMessage, 'error')
                return redirect(url_for('upload'))

            filename = secure_filename(file.filename)

            # Get valid username if submitted
            try:
                username = request.form.get('username').strip()[:20] # At most 20 characters
                if username == '':
                    raise AttributeError
            except (TypeError, AttributeError) as e:
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
            flash(successMessage, 'success')
            return redirect(url_for('upload'))

    return render_template('upload.html')


@app.route('/book/<int:_id>/', methods=['GET', 'POST'])
def bookPage(_id):
    b = Book()
    v = Vote()

    book = b.select(_id)
    if book is None:
        abort(404)

    if request.method == 'POST':

        try:
            vote = int(request.form.get('vote'))
        except (ValueError, TypeError) as e:
            flash('Invalid vote', 'error')
            return redirect(url_for('.bookPage', _id=_id))

        try:
            username = request.form.get('username').strip()[:20] # At most 20 characters
            if username == '':
                raise AttributeError
        except (TypeError, AttributeError) as e:
            username = None

        try:
            review = request.form.get('review').strip()[:500] # At most 500 characters
            if review == '':
                raise AttributeError
        except (TypeError, AttributeError) as e:
            review = None

        try:
            v.create(_id, vote, review, username)
        except ValueError as e:
            print('EXCEPTION HITTATA')
            flash('Invalid vote', 'error')
            return redirect(url_for('.bookPage', _id=_id))

        flash('Review added correctly')
        return redirect(url_for('.bookPage', _id=_id))

    return render_template('book.html', book=b.select(_id), reviews=v.pickRandom(_id), vote=v.avg(_id)['vote'])


@app.route('/book/<int:_id>/download/')
def bookDownload(_id):
    b = Book()
    book = b.select(_id)
    if book:
        return send_from_directory(app.config['UPLOAD_FOLDER'], book['name'])

    return redirect(url_for('home'))


if __name__ == '__main__':
    Schema()
    app.run(debug=True, host='0.0.0.0')
