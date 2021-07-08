from be.configuration import LABELS_TABLE_TYPE
from be.persistency.persistence_api import persistence_api


class VerticesLabels:
    EXCHANGE = "triangle"

    def __init__(self, configurations, address_to_id):
        self.address_to_id = address_to_id
        self.configurations = configurations


    def generate_shapes(self):
        # TODO this changes to triangles all vertices that are in the label list.
        # Change it to be exchanges.
        dex = persistence_api.get_labelled_vertices(self.configurations['graph_name'], LABELS_TABLE_TYPE, 'dex')
        idex = persistence_api.get_labelled_vertices(self.configurations['graph_name'], LABELS_TABLE_TYPE, 'idex')
        vertices = dex.append(idex)
        vertex_shapes = ['circle'] * len(self.address_to_id)
        for vertex in vertices['id'].values:
            vertex_shapes[vertex] = VerticesLabels.EXCHANGE
        return vertex_shapes
