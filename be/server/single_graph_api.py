import os

from flask import Blueprint, request, safe_join, send_from_directory
from werkzeug.routing import IntegerConverter
from be.configuration import CONFIGURATIONS, VERTEX_TABLE_NAME
from be.persistency.nice_abstraction import singletonNiceAbstraction
from be.utils.utils import wkt_to_x_y_list


class SignedIntConverter(IntegerConverter):
    regex = r'-?\d+'


single_graph_api = Blueprint('single_graph_api', __name__)

def check_graph_exists():
    graph_name = request.view_args['graph_name']
    if not singletonNiceAbstraction.is_graph_in_db(graph_name):
        raise Exception(f'It looks like the graph: {graph_name} was not correctly saved in the db.\n'
                        f'some or all db tables are missing, or have the wrong name.')


@single_graph_api.route(CONFIGURATIONS['endpoints']['graph_metadata'] + '/<graph_name>')
def get_graph_metadata(graph_name):
    metadata_frame = singletonNiceAbstraction.get_graph_metadata(graph_name)
    metadata_dictionary = metadata_frame.to_dict(orient='records')[0]
    return metadata_dictionary


@single_graph_api.route(CONFIGURATIONS['endpoints']['vertices_metadata'] + '/<graph_name>')
def get_nodes_metadata(graph_name):
    ids = singletonNiceAbstraction.get_labelled_vertices(graph_name)
    ids['st_astext'] = ids['st_astext'].apply(wkt_to_x_y_list).apply(tuple).apply(str)
    ids = ids.rename(columns={'st_astext': 'pos'})
    response = ids.to_dict(orient='records')
    return {'response': response}


@single_graph_api.route(
    CONFIGURATIONS['endpoints']['tile'] + '/<string:graph_name>/<signed_int:z>/<signed_int:x>/<signed_int:y>.png')
def get_tile(graph_name, z, x, y):
    # TODO move the imgs in the DB
    # print("recevied: " + str(z) + " " + str(x) + " " + str(y))

    tile_name = 'z_' + str(z) + 'x_' + str(x) + 'y_' + str(y) + '.png'
    source = os.path.join(CONFIGURATIONS['graphs_home'], graph_name)
    join = safe_join(source, tile_name)
    if os.path.isfile(os.path.join(source, tile_name)):
        return send_from_directory("../..", join, mimetype='image/jpeg')
    else:
        return 'Not present'


@single_graph_api.route(CONFIGURATIONS['endpoints']['edge_distributions'] + '/<graph_name>/<zoom_level>')
def get_distributions(graph_name, zoom_level):
    # TODO move the imgs in the DB
    path_join = os.path.join(CONFIGURATIONS['graphs_home'], graph_name)
    distribution_file_names = list(filter(lambda x: 'distribution' in x, os.listdir(path_join)))
    distribution_file_name = list(filter(lambda x: str(zoom_level) in x, distribution_file_names))[0]

    file = os.path.join(CONFIGURATIONS['graphs_home'], graph_name, distribution_file_name)
    return send_from_directory("../..", file, mimetype='image/jpeg')


@single_graph_api.route(
    CONFIGURATIONS['endpoints']['proximity_click'] + '/<graph_name>/<float(signed=True):x>/<float(signed=True):y>')
def get_closest_vertex(graph_name, x, y):
    # return str(x) + str(y) + str(graph_name)
    db_query_result = singletonNiceAbstraction.get_closest_point(x, y, VERTEX_TABLE_NAME(graph_name))
    eth = db_query_result['eth'][0]
    closest_point = wkt_to_x_y_list(db_query_result['st_astext'][0])
    size = db_query_result['size'][0]
    return {'eth': eth,
            'x': closest_point[0],
            'y': closest_point[1],
            'size': size}