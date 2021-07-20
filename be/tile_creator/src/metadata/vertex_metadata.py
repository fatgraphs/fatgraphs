import json

import requests


class VerticesLabels:
    EXCHANGE = "triangle"

    def __init__(self, configurations, address_to_id):
        self.address_to_id = address_to_id
        self.configurations = configurations


    def generate_shapes(self, graph_id):
        # TODO this changes to triangles all vertices that are in the label list.
        # Change it to be exchanges.
        dex_response = requests.get(f"http://localhost:5000/tokengallery/vertex/by/{graph_id}/type/dex")
        idex_response = requests.get(f"http://localhost:5000/tokengallery/vertex/by/{graph_id}/type/idex")
        dex = json.loads(dex_response.text)
        idex = json.loads(idex_response.text)
        dex.extend(idex)
        vertex_shapes = ['circle'] * len(self.address_to_id)
        for vertex in dex:
            match = self.address_to_id[self.address_to_id['address'] == vertex['eth']]
            index = match['vertex'].values[0]
            vertex_shapes[index] = VerticesLabels.EXCHANGE
        return vertex_shapes
