from flask import safe_join

class Tile:
    home_folder = "/home/carlo/tokengallery/be/graph-maps"

    def __init__(self, z: int, x: int, y: int):
        self.file_name = "z_{}x_{}y_{}.png".format(z, x, y)