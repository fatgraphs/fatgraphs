import pandas as pd


class VerticesLabels:
    EXCHANGE = "triangle"

    def __init__(self, configurations, address_to_id, vertex_positions):

        self.address_to_id = address_to_id

        if configurations['labels'] is not None:
            raw_labels = pd.read_csv(configurations['labels'])
            address_label_type = raw_labels[['address', 'label', 'type']]
            grouped_by_eth = self.remove_duplicate_eth(address_label_type)
            self.vertices_labels = grouped_by_eth \
                .merge(address_to_id, on="address") \
                .merge(vertex_positions).drop_duplicates()
        else:
            self.vertices_labels = pd.DataFrame(columns=['address', 'vertex', 'labels', 'types', 'x', 'y'])


    def generate_shapes(self):
        # TODO this changes to triangles all vertices that are in the label list.
        # Change it to be exchanges.
        vertex_shapes = ['circle'] * len(self.address_to_id)
        for vertex in self.vertices_labels['vertex'].values:
            vertex_shapes[vertex] = VerticesLabels.EXCHANGE
        return vertex_shapes

    def remove_duplicate_eth(self, raw_labels):
        """
        A vertex in the graph correpsonds to an eth address, it can have many types and labels associated.
        :param raw_labels:
        :return:
        """
        group_by_eth = raw_labels.groupby(by='address')\
            .agg(list)\
            .reset_index()\
            .rename(columns={'type': 'types', 'label': 'labels'})

        group_by_eth.types = group_by_eth.types.apply(tuple)
        group_by_eth.labels = group_by_eth.labels.apply(tuple)
        return group_by_eth
