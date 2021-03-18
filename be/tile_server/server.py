import os

from flask import Flask, send_file
from werkzeug.routing import IntegerConverter

from be.configuration import TILE_SOURCE


class SignedIntConverter(IntegerConverter):
    regex = r'-?\d+'


# before routes are registered
app = Flask(__name__)
app.url_map.converters['signed_int'] = SignedIntConverter


@app.route('/base_url/tms/1.0.0/test-graph/<signed_int:z>/<signed_int:x>/<signed_int:y>.png')
def hello_world(z, x, y):
    # print("recevied: " + str(z) + " " + str(x) + " " + str(y))

    tile_name = 'z_' + str(z) + 'x_' + str(x) + 'y_' + str(y) + '.png'
    tile_file = os.path.join(TILE_SOURCE, tile_name)
    if os.path.isfile(tile_file):
        return send_file(tile_file, mimetype='image/jpeg')
    else:
        return 'Not present'
