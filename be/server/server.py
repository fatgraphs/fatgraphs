import os

from flask import Flask
from flask import jsonify
from flask_cors import CORS
from werkzeug.routing import IntegerConverter, FloatConverter

from be.configuration import CONFIGURATIONS, LABELS_TABLE_TYPE, LABELS_TABLE_LABEL
from be.persistency.persistence_api import persistenceApi
from be.server.single_graph_api import singleGraphApi, check_graph_exists
from be.server.user_data_api import userDataApi


class SignedIntConverter(IntegerConverter):
    regex = r'-?\d+'


app = Flask(__name__)
app.url_map.converters['signed_int'] = SignedIntConverter
app.url_map.converters['float'] = FloatConverter
cors = CORS(app)

app.register_blueprint(singleGraphApi)
app.register_blueprint(userDataApi)
app.before_request_funcs = {
    'singleGraphApi': [check_graph_exists]
}

persistenceApi.ensureUserTableExists()
persistenceApi.ensureLabelsTableExists()


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return "This is the catch-all route.\nYou requested the URL: %s, but it didnt match anything" % path


@app.route(CONFIGURATIONS['endpoints']['availableGraphs'])
def getAvailableGraphs():
    graphNames = os.listdir(CONFIGURATIONS['graphsHome'])
    return jsonify(graphNames)


# TODO: for development return the exception to the client, remove in production
@app.errorhandler(Exception)
def serverError(err):
    app.logger.exception(err)
    return str(err)


@app.route(CONFIGURATIONS['endpoints']['autocompletionTerms'])
def getAutocompletionTerms():
    typesLabels = persistenceApi.getAllTypesAndLabels()
    uniqueTypes = typesLabels['type'].dropna().values
    uniqueLabels = typesLabels['label'].dropna().values

    response = list(map(lambda e: {'metadata_value': e,
                                   'metadata_type': LABELS_TABLE_TYPE},
                        uniqueTypes))

    response.extend(list(map(lambda e: {'metadata_value': e,
                                        'metadata_type': LABELS_TABLE_LABEL},
                             uniqueLabels)))

    return {'response': response}


@app.route(CONFIGURATIONS['endpoints']['addVertexMetadata'] + '/<eth>/<metadata_value>/<metadata_type>')
def add_vertex_metadata(eth, metadata_value, metadata_type):
    types_labels = persistenceApi.addVertexMetadata(eth, metadata_value, metadata_type)
    return {'response': 'ok'}
