import os

from flask import send_from_directory
from flask_restx import (
    Namespace,
    Resource,
    reqparse
)

from be.server.server import SessionLocal, app

from be.server.graph.service import GraphService
from be.server.tile.service import TileService

from functools import wraps


api = Namespace("Tile", description="Single namespace, single entity")  # noqa

# reqparser offers a nice interface to the content of the flask request object
image_upload_parser = reqparse.RequestParser()
image_upload_parser.add_argument(
    'image', 
    type=reqparse.FileStorage, 
    location='files', 
    required=True, 
    help='Image file to upload'
)


def mkdir_for_graph(graph_id: int):
    def ensure_directory_exists(path):
        if not os.path.exists(path):
            os.mkdir(path)

    ensure_directory_exists(app.config['TILES_HOME'])

    graph_folder = app.config['TILE_FOLDER_NAME'](graph_id)
    ensure_directory_exists(graph_folder)
    return graph_folder


def img_upload_middleware(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        args = image_upload_parser.parse_args()
        uploaded_file = args['image']

        if uploaded_file.mimetype not in ('image/png'):
            return {'message': 'Unsupported file type, must be image/png'}, 400
        else:
            return func(*args, **kwargs, image=uploaded_file)

    return decorated_function


@api.route("/<string:graph_id>/<signed_int:z>/<signed_int:x>/<signed_int:y>.png")
@api.param("graph_id", "Graph Id")
@api.param("z", "Zoom Level")
@api.param("x", "X coordinate")
@api.param("y", "Y coordinate")
class TileNameResource(Resource):

    def get(self, graph_id: int, z: int, x: int, y: int):
        with SessionLocal() as db:
            graph_folder = app.config['TILE_FOLDER_NAME'](graph_id)
            tile_name = TileService.get_tile_name(z, x, y)
            return send_from_directory(os.path.abspath(graph_folder), tile_name, mimetype='image/jpeg')
        
    @api.expect(image_upload_parser)
    @img_upload_middleware
    def post(self, graph_id: int, z: int, x: int, y: int, image):
        graph_tile_folder = mkdir_for_graph(graph_id)
        image.save(graph_tile_folder + '/' + TileService.get_tile_name(z, x, y))
        return 200



@api.route("/plot/<string:graph_id>/<signed_int:z>")
@api.param("graph_id", "Graph Id")
@api.param("z", "Zoom Level")
class EdgePlotsResource(Resource):

    def get(self, graph_id: int, z: int):
        with SessionLocal() as db:
            tile_folder = app.config['TILE_FOLDER_NAME'](graph_id)
            plot_name = "z_{}_distribution.png".format(z)

            return send_from_directory(
                os.path.abspath(tile_folder), 
                plot_name, 
                mimetype='image/jpeg'
            )
    
    @api.expect(image_upload_parser)
    @img_upload_middleware
    def post(self, graph_id: int, z: int, image):
        
        graph_tile_folder = mkdir_for_graph(graph_id)
        plot_name = f"z_{z}_distribution.png"
        image.save(graph_tile_folder + '/' + plot_name)

        return 200