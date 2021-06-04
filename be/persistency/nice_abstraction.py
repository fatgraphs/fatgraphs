from be.persistency.db_connection import DbConnection
from be.tile_creator.src.layout.visual_layout import VisualLayout
from be.persistency.implementation import Implementation

"""
This class exposes the methods that are used to interact with the persistency layer, 
hiding the detail in the implementaiton.
"""
class NiceAbstraction:

    def __init__(self, connection_string):
        self.connection = DbConnection(connection_string)
        self.impl = Implementation(self.connection)

    def persist_eth_positions(self, layout, graph_name):
        if not isinstance(layout, VisualLayout):
            raise Exception("Layout needs to be of type VisualLayout")
        edge_ids_to_positions = layout.edge_ids_to_positions.to_pandas()
        # instead of ids we need eth
        edge_ids_to_positions = edge_ids_to_positions.merge(layout.graph.address_to_id, left_on='source_id', right_on='vertex')
        edge_ids_to_positions = edge_ids_to_positions.drop(columns=['source_id', 'vertex'])
        edge_ids_to_positions = edge_ids_to_positions.rename(columns={'address': 'source_eth'})

        edge_ids_to_positions = edge_ids_to_positions.merge(layout.graph.address_to_id, left_on='target_id', right_on='vertex')
        edge_ids_to_positions = edge_ids_to_positions.drop(columns=['target_id', 'vertex'])
        edge_ids_to_positions = edge_ids_to_positions.rename(columns={'address': 'target_eth'})

        geopandas_frame = self.impl.to_geopandas(edge_ids_to_positions)

        table_name = graph_name + "_" + 'layout'
        self.impl.persist_geoframe(geopandas_frame, table_name)

    def get_closest_point(self, x, y, table):
        return self.impl.query_closest_point(x, y, table)

singletonNiceAbstraction = NiceAbstraction('postgresql://postgres:7412@127.0.0.1')