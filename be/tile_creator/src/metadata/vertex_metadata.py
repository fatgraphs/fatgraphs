import pandas as pd


class VerticesLabels:
    EXCHANGE = "triangle"

    def __init__(self, configurations, address_to_id, vertex_positions):

        self.address_to_id = address_to_id

        if configurations['labels'] is not None:
            raw_labels = pd.read_csv(configurations['labels'])
            address_label_type = raw_labels[['address', 'label', 'type']]
            self.vertices_labels = address_label_type \
                .merge(address_to_id, on="address") \
                .merge(vertex_positions).drop_duplicates()
        else:
            self.vertices_labels = pd.DataFrame(columns=['address', 'vertex', 'label', 'x', 'y'])


    def generate_shapes(self):
        # TODO this changes to triangles all vertices that are in the label list.
        # Change it to be exchanges.
        vertex_shapes = ['circle'] * len(self.address_to_id)
        for vertex in self.vertices_labels['vertex'].values:
            vertex_shapes[vertex] = VerticesLabels.EXCHANGE
        return vertex_shapes
