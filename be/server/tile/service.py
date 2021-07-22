from flask import safe_join, send_from_directory

from be.server.tile.model import Tile


class TileService:


    @staticmethod
    def get_tile_name(z: int, x: int, y: int) -> str:
        tile = Tile(z, x, y)
        return tile.file_name

    @classmethod
    def get_tile_folder(cls, graph_name, graph_id):
        return safe_join(Tile.home_folder, graph_name + '_' + graph_id)
