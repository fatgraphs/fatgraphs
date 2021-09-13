import os
from flask import send_from_directory
from flask_restx import Namespace, Resource
from .service import TileService
from .. import SessionLocal
from ..graph.service import GraphService

api = Namespace("Tile", description="Single namespace, single entity")  # noqa


@api.route("/<string:graph_id>/<signed_int:z>/<signed_int:x>/<signed_int:y>.png")
@api.param("graph_id", "Graph Id")
@api.param("z", "Zoom Level")
@api.param("x", "X coordinate")
@api.param("y", "Y coordinate")
class TileNameResource(Resource):

    def get(self, graph_id: int, z: int, x: int, y: int):
        with SessionLocal() as db:
            graph = GraphService.get_by_id(graph_id, db)
            graph_name = graph.graph_name
            tile_folder = TileService.get_tile_folder(graph_name, graph_id)
            tile_name = TileService.get_tile_name(z, x, y)
            return send_from_directory(os.path.abspath(tile_folder), tile_name, mimetype='image/jpeg')



@api.route("/plot/<string:graph_id>/<signed_int:z>")
@api.param("graph_id", "Graph Id")
@api.param("z", "Zoom Level")
class EdgePlotsResource(Resource):

    def get(self, graph_id: int, z: int):
        with SessionLocal() as db:
            graph = GraphService.get_by_id(graph_id, db)
            graph_name = graph.graph_name
            tile_folder = TileService.get_tile_folder(graph_name, graph_id)
            plot_name = "z_{}_distribution.png".format(z)
            return send_from_directory(os.path.abspath(tile_folder), plot_name, mimetype='image/jpeg')