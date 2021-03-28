import os
import pandas as pd
from flask import Flask, send_file
from werkzeug.routing import IntegerConverter
from flask_cors import CORS, cross_origin
from be.configuration import TILE_SOURCE, CONFIGURATIONS, METADATA_PATH


class SignedIntConverter(IntegerConverter):
    regex = r'-?\d+'


# before routes are registered
app = Flask(__name__)
cors = CORS(app)
app.url_map.converters['signed_int'] = SignedIntConverter

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
    if os.path.exists(METADATA_PATH):
        csv = pd.read_csv(METADATA_PATH)
    else:
        raise Exception("Create the metadata.csv file by running experiments/create_graph_metadata.py and moving "
                        "the generated file to the data folder")
    csv['pos'] = csv.apply(lambda row: (round(row['x'], 2), round(row['y'], 2)), axis=1)
    csv = csv.drop(columns=['x', 'y'])
    response = {}
    for i, r in csv.iterrows():
        response[str(r['pos'])] = [str(r['label']), str(r['address'])]
    return response


@app.route(CONFIGURATIONS['endpoints']['graph_summary'])
def get_graph_summary():
    # TODO: hardcoded for now
    return {"nodes": 456,
            "edges": 300}
