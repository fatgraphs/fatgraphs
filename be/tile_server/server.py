import os

from flask import Flask, send_file
from werkzeug.routing import IntegerConverter
from flask_cors import CORS, cross_origin
from be.configuration import TILE_SOURCE, CONFIGURATIONS


class SignedIntConverter(IntegerConverter):
    regex = r'-?\d+'


# before routes are registered
app = Flask(__name__)
cors = CORS(app)
app.url_map.converters['signed_int'] = SignedIntConverter


#TODO: define URLs in a JSON file global to BE and FE and read it

@app.route(CONFIGURATIONS['endpoints']['tile'] + '/<signed_int:z>/<signed_int:x>/<signed_int:y>.png')
def hello_world(z, x, y):
    # print("recevied: " + str(z) + " " + str(x) + " " + str(y))

    tile_name = 'z_' + str(z) + 'x_' + str(x) + 'y_' + str(y) + '.png'
    tile_file = os.path.join(TILE_SOURCE, tile_name)
    if os.path.isfile(tile_file):
        return send_file(tile_file, mimetype='image/jpeg')
    else:
        return 'Not present'


@app.route(CONFIGURATIONS['endpoints']['interest_points'])
def get_interest_points():
    # TODO: hardcoded for now
    return {'exchanges': [(-2, -2), (2, 2), (0, 0)],
            'half_graph_side' : 9999} # TODO