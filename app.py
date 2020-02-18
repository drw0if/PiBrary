# app.py

from flask import Flask
from models import Schema

app = Flask(__name__)

"""
get config
"""


@app.route('/')
def home():
    return 'Hello world!'


@app.route('/<name>')
def greet(name):
    return f'Hello {name}!'


if __name__ == '__main__':
    Schema()
    app.run(debug=True)
