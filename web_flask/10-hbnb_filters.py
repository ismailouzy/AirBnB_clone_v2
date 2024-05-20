#!/usr/bin/python3
"""
Airbnb clone flask application
"""


from models import storage
from models.state import State
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


@app.route('/states_list', strict_slashes=False)
def state_list():
    """displays states Tag in HTML
        args:
            @id: state id
            @name: state name
    """
    list_state = list(storage.all(State).values())
    list_state.sort(key=lambda x: x.name)
    states_dic = {
            'states': list_state
            }

    return render_template("7-states_list.html", **states_dic)


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    '''The cities_by_states page.'''
    state_dict = {
        'states': sorted(
            (state for state in storage.all(State).values()),
            key=lambda x: x.name
        )
    }
    for state in state_dict['states']:
        state.cities.sort(key=lambda x: x.name)
    return render_template('8-cities_by_states.html', **state_dict)


@app.route('/states', strict_slashes=False)
@app.route('/states/<id>', strict_slashes=False)
def states(id=None):
    '''The states page.'''
    list_state = {}
    all_states = sorted(
        (state for state in storage.all(State).values()),
        key=lambda x: x.name
    )
    if id is not None:
        state = next((state for state in all_states if state.id == id), None)
        if state:
            state.cities.sort(key=lambda x: x.name)
            list_state = {
                'state': state,
                'case': 2
            }
        else:
            list_state['case'] = 404
    else:
        for state in all_states:
            state.cities.sort(key=lambda x: x.name)
        list_state['states'] = all_states
        list_state['case'] = 1
    return render_template('9-states.html', **list_state)


@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_filters():
    '''The hbnb_filters page.'''
    list_state = {
        'states': sorted(
            (state for state in storage.all(State).values()),
            key=lambda x: x.name
        ),
        'amenities': sorted(
            (amenity for amenity in storage.all(Amenity).values()),
            key=lambda x: x.name
        )
    }
    for state in list_state['states']:
        state.cities.sort(key=lambda x: x.name)
    return render_template('10-hbnb_filters.html', **list_state)


@app.teardown_appcontext
def teardown_app(appexc):
    """close the storage session"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
