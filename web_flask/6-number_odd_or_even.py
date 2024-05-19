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


@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_text(text="is cool"):
    """python directory in the website
        args:
            @text: a string with a default value
    """
    return f"Python {text.replace('_', ' ')}"


@app.route('/number/<n>', strict_slashes=False)
def number(n):
    """number directory in the website
        args:
            @n: integer"""
    if n is not None:
        try:
            n = int(n)
            return f"{n} is a number"
        except ValueError:
            pass
    abort(404)


@app.route('/number_template/<n>', strict_slashes=False)
def number_template(n):
    """number template func that desplate an HTML page if n arg is an int
        args:
            @n: an integer
    """
    if n is not None:
        try:
            n = int(n)
            return render_template("5-number.html", n=n)
        except ValueError:
            pass
        abort(404)


@app.route('/number_odd_or_even/<n>', strict_slashes=False)
def number_oddoreven(n):
    """Displays if the number n is Odd or even
        args:
            @n: integer
    """
    if n is not None:
        try:
            n = int(n)
            return render_template("6-number_odd_or_even.html", n=n)
        except ValueError:
            pass
        abort(404)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
