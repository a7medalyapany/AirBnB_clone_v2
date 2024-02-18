#!/usr/bin/python3
""" Module to start a Flask web application"""

from flask import Flask


app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/')
def hello_world():
    """ Gimme some text. """
    return 'Hello HBNB!'


@app.route('/hbnb')
def hello():
    """ Gimme other text. """
    return 'HBNB'


@app.route('/c/<text>')
def c_text(text):
    """ text -> variable. """
    text = text.replace('_', ' ')
    return 'C {}'.format(text)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
