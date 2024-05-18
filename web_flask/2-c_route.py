#!/usr/bin/python3
"""
Airbnb clone flask application
"""

from flask import Flask, abort, request, render_template
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index():
    """index page of the Airbnb clone"""
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def HBNB():
    """HBNB directory in the Airbnb clone"""
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def C_is_fun(text):
    """C directory
        args:
            @text: string
    """
    return f"C {text.replace('_', ' ')}"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
