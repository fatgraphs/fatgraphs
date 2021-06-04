import os
from flask import jsonify, send_from_directory
from flask import Flask, send_file, safe_join
from werkzeug.routing import IntegerConverter, FloatConverter
from flask_cors import CORS, cross_origin
from be.configuration import CONFIGURATIONS, LAYOUT_DB_TABLE
import pandas as pd

from be.persistency.nice_abstraction import singletonNiceAbstraction


class SignedIntConverter(IntegerConverter):
    regex = r'-?\d+'


# before routes are registered
app = Flask(__name__)
cors = CORS(app)
app.url_map.converters['signed_int'] = SignedIntConverter
app.url_map.converters['float'] = FloatConverter


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return "This is the catch-all route.\nYou requested the URL: %s, but it didnt match anything" % path


@app.route(CONFIGURATIONS['endpoints']['available_graphs'])
def get_available_graphs():
    graph_names = os.listdir(CONFIGURATIONS['graphs_home'])
    return jsonify(graph_names)


@app.route(
    CONFIGURATIONS['endpoints']['tile'] + '/<string:graph_name>/<signed_int:z>/<signed_int:x>/<signed_int:y>.png')
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
    metadata_dictionary = csv.to_dict(orient='records')[0]
    metadata_dictionary['labels'] = str(metadata_dictionary['labels'])
    return metadata_dictionary


@app.route(CONFIGURATIONS['endpoints']['edge_distributions'] + '/<graph_name>/<zoom_level>')
def get_distributions(graph_name, zoom_level):
    path_join = os.path.join(CONFIGURATIONS['graphs_home'], graph_name)
    distribution_file_names = list(filter(lambda x: 'distribution' in x, os.listdir(path_join)))
    distribution_file_name = list(filter(lambda x: str(zoom_level) in x, distribution_file_names))[0]

    file = os.path.join(CONFIGURATIONS['graphs_home'], graph_name, distribution_file_name)
    return send_from_directory("../..", file, mimetype='image/jpeg')


@app.route(
    CONFIGURATIONS['endpoints']['proximity_click'] + '/<graph_name>/<float(signed=True):x>/<float(signed=True):y>')
def get_closest_vertex(graph_name, x, y):
    # return str(x) + str(y) + str(graph_name)
    db_query_result = singletonNiceAbstraction.get_closest_point(x, y, LAYOUT_DB_TABLE(graph_name))
    closest_point = db_query_result[1].split('(')[-1].split(')')[0].split(' ')
    return {'eth': db_query_result[0],
            'x': closest_point[0],
            'y': closest_point[1]}
