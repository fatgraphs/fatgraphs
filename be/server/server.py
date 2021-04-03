import os
from flask import jsonify
from flask import Flask, send_file
from werkzeug.routing import IntegerConverter
from flask_cors import CORS, cross_origin
from be.configuration import CONFIGURATIONS, GRAPHS_HOME
import pandas as pd

class SignedIntConverter(IntegerConverter):
    regex = r'-?\d+'


# before routes are registered
app = Flask(__name__)
cors = CORS(app)
app.url_map.converters['signed_int'] = SignedIntConverter


@app.route(CONFIGURATIONS['endpoints']['available_graphs'])
def get_available_graphs():
    graph_names = os.listdir(GRAPHS_HOME)
    return jsonify(graph_names)


@app.route(CONFIGURATIONS['endpoints']['tile'] + '/<graph_name>' + '/<signed_int:z>/<signed_int:x>/<signed_int:y>.png')
def get_tile(graph_name, z, x, y):
    # print("recevied: " + str(z) + " " + str(x) + " " + str(y))

    tile_name = 'z_' + str(z) + 'x_' + str(x) + 'y_' + str(y) + '.png'
    source = os.path.join(GRAPHS_HOME, graph_name)
    tile_file = os.path.join(source, tile_name)
    if os.path.isfile(tile_file):
        return send_file(tile_file, mimetype='image/jpeg')
    else:
        return 'Not present'


@app.route(CONFIGURATIONS['endpoints']['vertices_metadata'] + '/<graph_name>')
def get_nodes_metadata(graph_name):
    graph_source = os.path.join(GRAPHS_HOME, graph_name)
    if os.path.exists(source):
        csv = pd.read_csv(source)
    else:
        raise Exception("The metadata.csv file fro the graph is missing")
    csv['pos'] = csv.apply(lambda row: (round(row['x'], 2), round(row['y'], 2)), axis=1)
    csv = csv.drop(columns=['x', 'y'])
    response = {}
    for i, r in csv.iterrows():
        response[str(r['pos'])] = [str(r['label']), str(r['address'])]
    return response


@app.route(CONFIGURATIONS['endpoints']['graph_metadata'])
def get_graph_metadata():
    if os.path.exists(VERTICES_METADATA_PATH):
        csv = pd.read_csv(GRAPH_METADATA_PATH)
    else:
        raise Exception("The vertices metadata file is missing")
    # TODO: save nodes and edges and dont hardcode
    return {"name": csv['name'][0],
            "vertices": int(csv['vertices'][0]),
            "edges": int(csv['edges'][0]),
            "min_coordinate": csv['min'][0],
            "max_coordinate": csv['max'][0]}
