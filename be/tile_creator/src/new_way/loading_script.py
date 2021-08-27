from be.tile_creator.src.new_way.cudf_graph import CudfGraph
from be.tile_creator.src.new_way.datasource import DataSource
from be.tile_creator.src.new_way.edge_data import EdgeData
from be.tile_creator.src.new_way.graph_data import GraphData
from be.tile_creator.src.new_way.gtm_args import GtmArgs
from be.tile_creator.src.new_way.vertex_data import VertexData

gtm_args = GtmArgs()

source = DataSource('../../../../data/medium.csv')

vertex_data = VertexData()
edge_data = EdgeData()
graph_data = GraphData()

vertex_data.set_vertex_to_ids(source)
edge_data.set_source_target_amount(source, vertex_data.get_vertex_to_id())
# edge_data.populate_source_target_amount_cudf()

cudf_graph = CudfGraph(edge_data.get_source_target_amount())

vertex_data.set_degrees(cudf_graph.get_graph())
vertex_data.set_positions(cudf_graph.get_graph())

graph_data.set_bounding_square(vertex_data.get_positions())
graph_data.set_bounding_square_pixel(gtm_args)

vertex_data.set_positions_pixel(gtm_args, graph_data)

vertex_data.set_fake_positions(graph_data)

edge_data.set_ids_to_position(vertex_data.get_positions(cudf=True))
edge_data.set_ids_to_pixel_position(vertex_data.get_positions_pixel())

graph_data.set_median_pixel_distance(vertex_data.get_positions_pixel())

edge_data.set_thickness(graph_data, gtm_args)
