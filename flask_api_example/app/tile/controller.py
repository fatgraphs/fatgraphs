from flask import send_from_directory
from flask_restx import Namespace, Resource
from .service import TileService

api = Namespace("Tile", description="Single namespace, single entity")  # noqa


@api.route("/tile/<string:graph_name>/<signed_int:z>/<signed_int:x>/<signed_int:y>.png")
@api.param("graph_name", "Tile Name")
@api.param("z", "Zoom Level")
@api.param("x", "X coordinate")
@api.param("y", "Y coordinate")
class TileNameResource(Resource):

    def get(self, graph_name: str, z: int, x: int, y: int):
        tile_home = TileService.get_tile_folder(graph_name)
        tile_name = TileService.get_tile_name(graph_name, z, x, y)
        return send_from_directory(tile_home, tile_name, mimetype='image/jpeg')

