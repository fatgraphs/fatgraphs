from flask import safe_join, send_from_directory

from flask_api_example.app.tile.model import Tile


class TileService:

    @staticmethod
    def get_tile_folder(graph_name: str) -> str:
        return Tile.home_folder

    @staticmethod
    def get_tile_name(graph_name: str, z: int, x: int, y: int) -> str:
        tile = Tile(graph_name, z, x, y)
        return tile.file_path
