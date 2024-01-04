#!/usr/bin/python3
""" A scrip that starts a flask web app """
from models import storage
from models.state import State
from flask import Flask
from flask import render_template
app = Flask(__name__)


# Define a function to be called when the application context is torn down
@app.teardown_appcontext
def hbnb_db(error):
    """ remove the current SQLAlchemy Session """
    storage.close()


@app.route('/states_list', strict_slashes=False)
def states_list():
    # Retrieve all State objects from the storage (presumably a database)
    states = storage.all(State).values()

    # Sort the list of states based on the 'name'
    # attribute of each State object
    states = sorted(states, key=lambda k: k.name)
    return render_template('7-states_list.html', states=states)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
