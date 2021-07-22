from be.server.vertex.service import VertexService


class VerticesLabels:
    EXCHANGE = "triangle"

    def __init__(self, configurations, address_to_id):
        self.address_to_id = address_to_id
        self.configurations = configurations


    def generate_shapes(self, graph_id, db):

        idex = VertexService.get_by_type(graph_id, 'idex', db)
        dex = VertexService.get_by_type(graph_id, 'dex', db)

        dex.extend(idex)
        vertex_shapes = ['circle'] * len(self.address_to_id)
        for vertex in dex:
            match = self.address_to_id[self.address_to_id['address'] == vertex.eth]
            index = match['vertex'].values[0]
            vertex_shapes[index] = VerticesLabels.EXCHANGE
        return vertex_shapes
