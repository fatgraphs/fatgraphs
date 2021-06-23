import os

from flask import Flask
from flask import jsonify
from flask_cors import CORS
from werkzeug.routing import IntegerConverter, FloatConverter

from be.configuration import CONFIGURATIONS
from be.persistency.persistence_api import persistence_api
from be.server.single_graph_api import single_graph_api, check_graph_exists
from be.server.user_data_api import user_data_api


class SignedIntConverter(IntegerConverter):
    regex = r'-?\d+'


# before routes are registered
app = Flask(__name__)
app.url_map.converters['signed_int'] = SignedIntConverter
app.url_map.converters['float'] = FloatConverter
cors = CORS(app)

app.register_blueprint(single_graph_api)
app.register_blueprint(user_data_api)
app.before_request_funcs = {
    'single_graph_api': [check_graph_exists]
}

persistence_api.ensure_user_table_exists()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return "This is the catch-all route.\nYou requested the URL: %s, but it didnt match anything" % path


@app.route(CONFIGURATIONS['endpoints']['available_graphs'])
def get_available_graphs():
    graph_names = os.listdir(CONFIGURATIONS['graphs_home'])
    return jsonify(graph_names)


# TODO: for development return the exception to the client, remove in production
@app.errorhandler(Exception)
def server_error(err):
    app.logger.exception(err)
    return str(err)
