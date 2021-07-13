import os

from flask import Blueprint, request, safe_join, send_from_directory
from werkzeug.routing import IntegerConverter
from be.configuration import CONFIGURATIONS, VERTEX_TABLE_NAME
from be.persistency.persistence_api import persistenceApi
from be.utils.utils import wktToXYList


class SignedIntConverter(IntegerConverter):
    regex = r'-?\d+'


singleGraphApi = Blueprint('singleGraphApi', __name__)


def checkGraphExists():
    graphName = request.view_args['graphName']
    if not persistenceApi.isGraphInDb(graphName):
        raise Exception(f'It looks like the graph: {graphName} was not correctly saved in the db.\n'
                        f'some or all db tables are missing, or have the wrong name.')


@singleGraphApi.route(CONFIGURATIONS['endpoints']['graphMetadata'] + '/<graphName>')
def getGraphMetadata(graphName):
    metadataFrame = persistenceApi.getGraphMetadata(graphName)
    metadataDictionary = metadataFrame.to_dict(orient='records')[0]
    return metadataDictionary


@singleGraphApi.route(CONFIGURATIONS['endpoints']['matchingVertex']
                        + '/<graphName>/<searchMethod>/<searchQuery>')
def getMatchingVertices(graphName, searchMethod, searchQuery):
    """
    :param graph_name:
    :param search_method: what field to use in the search
    :param search_query: what value to match against
    :return: Returns a list of vertices (objects with position, eth, label and type)
    matching the search method (e.g. type == dex).
    For each eth matching the provided conditions it ALSO FETCHES ALL THE LABELS AND TYPES (which you may not have asked for).
    """
    if searchMethod not in ['type', 'label', 'eth']:
        raise Exception("search method is not valid.")
    ids = persistenceApi.getLabelledVertices(graphName, searchMethod, searchQuery)
    ids = ids.drop_duplicates()  # TODO remove duplicates before this point
    if ids.empty:
        response = []
    else:
        for eth in ids['eth']:
            vertices = persistenceApi.getLabelledVertices(graphName, 'eth', eth)
            ids = ids.append(vertices)

        ids['st_astext'] = ids['st_astext'].apply(wktToXYList).apply(tuple).apply(str)
        ids = ids.rename(columns={'st_astext': 'pos'})

        ids = ids.drop_duplicates()
        response = ids.to_dict(orient='records')
    return {'response': response}


@singleGraphApi.route(
    CONFIGURATIONS['endpoints']['tile'] + '/<string:graphName>/<signed_int:z>/<signed_int:x>/<signed_int:y>.png')
def getTile(graphName, z, x, y):
    # TODO move the imgs in the DB
    # print("recevied: " + str(z) + " " + str(x) + " " + str(y))

    tileName = 'z_' + str(z) + 'x_' + str(x) + 'y_' + str(y) + '.png'
    source = os.path.join(CONFIGURATIONS['graphsHome'], graphName)
    join = safe_join(source, tileName)
    if os.path.isfile(os.path.join(source, tileName)):
        return send_from_directory("../..", join, mimetype='image/jpeg')
    else:
        return 'Not present'


@singleGraphApi.route(CONFIGURATIONS['endpoints']['edgeDistributions'] + '/<graphName>/<zoomLevel>')
def getDistributions(graphName, zoomLevel):
    # TODO move the imgs in the DB
    pathJoin = os.path.join(CONFIGURATIONS['graphsHome'], graphName)
    distributionFileNames = list(filter(lambda x: 'distribution' in x, os.listdir(pathJoin)))
    distributionFileName = list(filter(lambda x: str(zoomLevel) in x, distributionFileNames))[0]

    file = os.path.join(CONFIGURATIONS['graphsHome'], graphName, distributionFileName)
    return send_from_directory("../..", file, mimetype='image/jpeg')


@singleGraphApi.route(
    CONFIGURATIONS['endpoints']['proximityClick'] + '/<graphName>/<float(signed=True):x>/<float(signed=True):y>')
def getClosestVertex(graphName, x, y):
    # return str(x) + str(y) + str(graph_name)
    dbQueryResult = persistenceApi.getClosestVertex(x, y, graphName)
    eth = dbQueryResult['eth'][0]
    closestPointPos = wkt_to_x_y_list(dbQueryResult['st_astext'][0])
    size = dbQueryResult['size'][0]
    metadata = persistenceApi.getLabelledVertices(graphName, 'eth', eth).drop_duplicates()
    vertexTypes = []
    vertexLabels = []
    if not metadata.empty:
        vertexTypes = list(metadata['type'].values)
        vertexLabels = list(metadata['label'].values)
    return {'eth': eth,
            'pos': closestPointPos,
            'size': size,
            'types': vertexTypes,
            'labels': vertexLabels}
