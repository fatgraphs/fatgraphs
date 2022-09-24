from be.configuration import CONFIGURATIONS

class Tile:
    home_folder = CONFIGURATIONS['graphsHome']

    def __init__(self, z: int, x: int, y: int):
        self.file_name = "z_{}x_{}y_{}.png".format(z, x, y)