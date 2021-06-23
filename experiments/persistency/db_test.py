import geopandas as gpd
from geoalchemy2 import Geometry, WKTElement
from sqlalchemy import *

from be.tile_creator.src.graph.token_graph import TokenGraph
from be.tile_creator.src.layout.visual_layout import VisualLayout
from be.tile_creator.src.metadata.vertex_metadata import VerticesLabels
from be.tile_creator.src.render.transparency_calculator import TransparencyCalculator


"""
This is experimental/throw-away code that served as initial experimentation with the postgtres GIS DB.
To run it substitute the call to main with a call to mainn in the gtm.py script.

The functions have been named with 'calro' in order to find them more easily in the IDE profiler.
"""

def mainn(configurations):
    graph_layout = load_graph_as_usual(configurations)
    # to_pandas_time = datetime.datetime.now()
    pandas_1 = to_pandas_carlo(graph_layout)
    # print("to pandas took ms:")
    # print((datetime.datetime.now() - to_pandas_time).microseconds / 1000)

    # Creating SQLAlchemy's engine to use
    engine = create_engine('postgresql://postgres:7412@127.0.0.1')
    # pandas_frame = pd.DataFrame(columns=['eth', 'x', 'y'],
    #                             data=[['0x12345', 2, 2], ['0x12345678', -2, -2.55]])
    # geodataframe = gpd.GeoDataFrame(pandas_frame,
    #                                 geometry=gpd.points_from_xy(pandas_frame.x, pandas_frame.y))

    # to_geopandas_time = datetime.datetime.now()
    geopandas_2 = to_geopandas_carlo(pandas_1)
    #
    # print("to GEO pandas took ms:")
    # print((datetime.datetime.now() - to_geopandas_time).microseconds / 1000)

    # to_db = datetime.datetime.now()
    # gdf = geodataframe.drop(columns=['x', 'y', 'geometry'])
    to_db_carlo(engine, geopandas_2)
    # print("to db took ms:")
    # print((datetime.datetime.now() - to_db).microseconds / 1000)


def to_pandas_carlo(graph_layout):
    pandas_1 = graph_layout.edge_ids_to_positions.to_pandas()
    return pandas_1


def to_geopandas_carlo(pandas_1):
    source_geo = gpd.GeoDataFrame(pandas_1,
                                  geometry=gpd.points_from_xy(pandas_1.source_x, pandas_1.source_y))
    source_geo = source_geo.rename_geometry('source_geo')
    target_geo = gpd.GeoDataFrame(pandas_1,
                                  geometry=gpd.points_from_xy(pandas_1.target_x, pandas_1.target_y))
    target_geo = target_geo.rename_geometry('target_geo')
    geopandas_2 = source_geo.merge(target_geo).drop(columns=['source_x', 'source_y', 'target_x', 'target_y'])
    geopandas_2['source_geo'] = geopandas_2['source_geo'].apply(lambda x: WKTElement(x.wkt, srid=3857))
    geopandas_2['target_geo'] = geopandas_2['target_geo'].apply(lambda x: WKTElement(x.wkt, srid=3857))
    return geopandas_2


def to_db_carlo(engine, geopandas_2):
    geopandas_2.to_sql("vero5", engine,
                       if_exists='append',
                       index=False,
                       dtype={'source_geo': Geometry('POINT', srid=3857),
                              'target_geo': Geometry('POINT', srid=3857)})


def load_graph_as_usual(configurations):
    global vertices_labels, visual_layout
    graph = TokenGraph(configurations['source'], {'dtype': {'amount': float}})
    visual_layout = VisualLayout(graph, configurations)
    vertices_labels = VerticesLabels(configurations, graph.address_to_id, visual_layout.vertex_positions)
    transparency_calculator = TransparencyCalculator(visual_layout.max - visual_layout.min,
                                                     configurations)
    visual_layout.edge_transparencies = transparency_calculator.calculate_edge_transparencies(
        visual_layout.edge_lengths)
    visual_layout.vertex_shapes = vertices_labels.generate_shapes()
    return visual_layout
# geoalchemy2.types._GISType.GEOMETRY
