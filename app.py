# app.py

from flask import Flask, render_template
from models import Schema, Book

app = Flask(__name__)

"""
get config
"""


@app.route('/')
def home():
    B = Book()
    return render_template('home.html', books = B.select())

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    pass


if __name__ == '__main__':
    Schema()
    app.run(debug=True)
