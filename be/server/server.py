import os
from flask import jsonify, send_from_directory
from flask import Flask, send_file, safe_join
from werkzeug.routing import IntegerConverter
from flask_cors import CORS, cross_origin
from be.configuration import CONFIGURATIONS
import pandas as pd

class SignedIntConverter(IntegerConverter):
    regex = r'-?\d+'


# before routes are registered
app = Flask(__name__)
cors = CORS(app)
app.url_map.converters['signed_int'] = SignedIntConverter


@app.route(CONFIGURATIONS['endpoints']['available_graphs'])
def get_available_graphs():
    graph_names = os.listdir(CONFIGURATIONS['graphs_home'])
    return jsonify(graph_names)


@app.route(CONFIGURATIONS['endpoints']['tile'] + '/<string:graph_name>/<signed_int:z>/<signed_int:x>/<signed_int:y>.png')
def get_tile(graph_name, z, x, y):
    # print("recevied: " + str(z) + " " + str(x) + " " + str(y))

    tile_name = 'z_' + str(z) + 'x_' + str(x) + 'y_' + str(y) + '.png'
    source = os.path.join(CONFIGURATIONS['graphs_home'], graph_name)
    join = safe_join(source, tile_name)
    if os.path.isfile(os.path.join(source, tile_name)):
        return send_from_directory("../..", join, mimetype='image/jpeg')
    else:
        return 'Not present'


@app.route(CONFIGURATIONS['endpoints']['vertices_metadata'] + '/<graph_name>')
def get_nodes_metadata(graph_name):
    source = os.path.join(CONFIGURATIONS['graphs_home'], graph_name, CONFIGURATIONS['vertices_metadata_file_name'])
    if os.path.exists(source):
        csv = pd.read_csv(source)
    else:
        raise Exception("The metadata.csv file fro the graph is missing")
    if csv.empty:
        return {}
    csv['pos'] = csv.apply(lambda row: (round(row['x'], 2), round(row['y'], 2)), axis=1)
    csv = csv.drop(columns=['x', 'y'])
    response = {}
    for i, r in csv.iterrows():
        response[str(r['pos'])] = [str(r['label']), str(r['address'])]
    return response


@app.route(CONFIGURATIONS['endpoints']['graph_metadata'] + '/<graph_name>')
def get_graph_metadata(graph_name):
    source = os.path.join(CONFIGURATIONS['graphs_home'], graph_name, CONFIGURATIONS['graph_metadata_file_name'])
    if os.path.exists(source):
        csv = pd.read_csv(source)
    else:
        raise Exception("The vertices metadata file is missing")
    return {"vertices": int(csv['vertices'][0]),
            "edges": int(csv['edges'][0]),
            "min_coordinate": csv['min'][0],
            "max_coordinate": csv['max'][0],
            "zoom_levels": int(csv['zoom_levels'][0]),
            "median_pixel_distance": float(csv["median_pixel_distance"][0])
            }
