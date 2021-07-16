from os.path import join

from flask import safe_join
from sqlalchemy import Integer, Column, String, Float, ForeignKey
from app import db  # noqa
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship, backref


class Tile:
    home_folder = "/home/carlo/tokengallery/be/graph-maps"

    def __init__(self, graph_name: str, z: int, x: int, y: int):
        self.file_path = safe_join(graph_name, "z_{}x_{}y_{}.png".format(z, x, y))