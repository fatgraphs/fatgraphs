import cugraph
import numpy as np
from cuml.neighbors.nearest_neighbors import NearestNeighbors
import cudf
from be.configuration import internal_id, CONFIGURATIONS
from be.server.vertex_metadata.service import VertexMetadataService

from be.utils import shift_and_scale, convert_graph_coordinate_to_map
import time

class VisualLayout:
    defaultForceAtlas2Options = {'max_iter': 500,
                                 'strong_gravity_mode': True,
                                 'barnes_hut_theta': 1.2,
                                 'outbound_attraction_distribution': False,
                                 'gravity': 1,
                                 'scaling_ratio': 1}

    def __init__(self, graph, config):
        self.graph = graph

        self.vertexPositions = self.runForceAtlas2(graph.gpuFrame)

        self.max = max(self.vertexPositions[0:-2]['x'].max(), self.vertexPositions[0:-2]['y'].max())
        self.min = min(self.vertexPositions[0:-2]['x'].min(), self.vertexPositions[0:-2]['y'].min())

        self.ensureLayoutIsSquare()
        self.edgeIdsToPositions = self.makeEdgeIdsToPositions()
        self.edgeIdsToPositionsPixel = self.convertToPixelSpace(config['tile_size'], self.min, self.max)
        self.edgeLengths = self.calculateEdgeLengthsGraphSpace()
        self.medianPixelDistance = self.computeMedianPixelDistance()
        self.vertexSizes = self.calculateVerticesSize(graph.degrees['inDegree'], config['med_vertex_size'],
                                                      config['max_vertex_size'])
        self.edgeThickness = self.calculate_edge_thickness(config, graph)

        self.edgeTransparencies = {}
        self.vertexShapes = None

    def calculate_edge_thickness(self, config, graph):
        logAmounts = np.log10(
            graph.edge_ids_to_amount['amount'].values + 1)  # amounts can be huge numbers, reduce the range
        return self.calculateEdgesThickness(logAmounts, config['med_edge_thickness'],
                                                          config['max_edge_thickness'])

    def runForceAtlas2(self, gpuGraph):

        # layout: x y vertex
        layout = cugraph.layout.force_atlas2(gpuGraph, **self.defaultForceAtlas2Options)
        layout = layout.to_pandas()
        # layout = self._distribute_on_square_edges(layout)
        layout = layout.sort_values(['vertex'])
        layout = layout.reset_index(drop=True)
        layout = layout.rename(columns={
            'vertex': CONFIGURATIONS['vertex_internal_id']
        })
        return layout

    def computeMedianPixelDistance(self):
        verticesOnce = self.edgeIdsToPositionsPixel.drop_duplicates(['sourceX', 'sourceY']).to_pandas()
        model = NearestNeighbors(n_neighbors=3)
        model.fit(verticesOnce[['sourceXPixel', 'sourceYPixel']])
        distances, indices = model.kneighbors(verticesOnce[['sourceXPixel', 'sourceYPixel']])
        medianPixelDistance = np.median(distances.flatten())
        return medianPixelDistance

    def ensureLayoutIsSquare(self):
        lastVertexId = self.vertexPositions[CONFIGURATIONS['vertex_internal_id']].max()
        penultimum_vertex_id = lastVertexId - 1
        self.vertexPositions.iloc[lastVertexId, 0:3] = [self.min, self.min, self.vertexPositions.iloc[lastVertexId, 0:3][2]]
        self.vertexPositions.iloc[penultimum_vertex_id, 0:3] = [self.max, self.max, self.vertexPositions.iloc[penultimum_vertex_id, 0:3][2]]

    def calculateVerticesSize(self, inDegrees, medVertexSize, maxVertexSize):
        targetMedian = self.medianPixelDistance * medVertexSize
        targetMax = self.medianPixelDistance * maxVertexSize
        return shift_and_scale(inDegrees, targetMedian, targetMax)

    def calculateEdgesThickness(self, amounts, medEdgeThickness, maxEdgeThickness):
        targetMedian = self.medianPixelDistance * medEdgeThickness
        targetMax = self.medianPixelDistance * maxEdgeThickness
        return shift_and_scale(amounts, targetMedian, targetMax)

    def calculateEdgeLengthsGraphSpace(self):
        distances = ((self.edgeIdsToPositions['sourceX'] - self.edgeIdsToPositions['targetX']) ** 2 + (
                self.edgeIdsToPositions['sourceY'] - self.edgeIdsToPositions['targetY']) ** 2) ** 0.5
        return distances.to_array()

    def makeEdgeIdsToPositions(self):
        vertexXY = cudf.from_pandas(self.vertexPositions)

        vertexXY = vertexXY.rename(columns={'x': 'sourceX', 'y': 'sourceY'})

        graphPositions = self.graph.edge_ids_to_amount_cudf \
            .merge(vertexXY, left_on=internal_id('source'), right_on=CONFIGURATIONS['vertex_internal_id']) \
            .drop(columns=[CONFIGURATIONS['vertex_internal_id']])

        vertexXY = vertexXY.rename(columns={'sourceX': 'targetX', 'sourceY': 'targetY'})

        graphPositions = graphPositions \
            .merge(vertexXY, left_on=internal_id('target'), right_on=CONFIGURATIONS['vertex_internal_id']) \
            .drop(columns=[CONFIGURATIONS['vertex_internal_id']])

        graphPositions = graphPositions\
            .sort_values(by=[internal_id('source'), internal_id('target')])\
            .reset_index(drop=True)

        return graphPositions

    def convertToPixelSpace(self, tileSize, minCoordinate, maxCoordinate):
        tileCoordinates = self.edgeIdsToPositions.apply_rows(convert_graph_coordinate_to_map,
                                                             incols=['sourceX', 'sourceY', 'targetX',
                                                                    'targetY'],
                                                             outcols=dict(sourceXPixel=np.float64,
                                                                         sourceYPixel=np.float64,
                                                                         targetXPixel=np.float64,
                                                                         targetYPixel=np.float64),
                                                             kwargs={'tileSize': tileSize,
                                                                    'minCoordinate': minCoordinate,
                                                                    'maxCoordinate': maxCoordinate})
        return tileCoordinates

    def distributeOnSquareEdges(self, layout):
        '''
        The layout generated by fa2 is a circle but the canvas is a rectangle.
        Therefore the corners of the rectangle won't have any node.
        We rectangularise the circular layout in order to better spread out the nodes.
        '''

        def scale(array, a, b):
            return (b - a) * ((array - min(array)) / max(1, (max(array) - min(array)))) + a

        # the layout is circular # to use more of the rectangular space, project onto a square
        u = layout["x"]
        v = layout["y"]
        umax = u.max()
        umin = u.min()
        vmax = v.max()
        vmin = v.min()

        # https://stats.stackexchange.com/a/178629

        u = scale(u, -0.9, 0.9)
        v = scale(v, -0.9, 0.9)

        # https://stackoverflow.com/a/32391780
        sqrtTwo = np.sqrt(2)
        x = (0.5 * np.sqrt(2 + (u * u) - (v * v) + 2 * u * sqrtTwo)) - (
                0.5 * np.sqrt(2 + (u * u) - (v * v) - 2 * u * sqrtTwo))
        y = (0.5 * np.sqrt(2 - (u * u) + (v * v) + 2 * v * sqrtTwo)) - (
                0.5 * np.sqrt(2 - (u * u) + (v * v) - 2 * v * sqrtTwo))
        # for small graphs the above equation can produce nans
        x = np.nan_to_num(x)
        y = np.nan_to_num(y)
        x = scale(x, umin, umax)
        y = scale(y, vmin, vmax)
        layout["x"] = x
        layout["y"] = y
        return layout

    def generate_shapes(self, db, graph_id):

        start_time = time.monotonic()

        def mark_token_icons():
            result['type_code'] = np.where(result['icon'].isnull(), result['type_code'], result['icon'])

        def mark_labelled():
            result['type'] = result['type'].where(result['type'].notna(), 0)
            # increment by 1 where type is not 0 (i.e. type == 'exchange')
            result['type_code'] = result['type_code'] + result['type'].where(result['type'] == 0, 1)

        icon_to_int = {
            'inactive_fake': 0,
            'eoa_unlabelled': 1,
            'eoa_labelled': 2,
            'ca_unlabelled': 3,
            'ca_labelled': 4,
        }
        int_to_icon = {v: k for k, v in icon_to_int.items()}

        account_types = VertexMetadataService.merge_graph_vertices_with_account_type(db, graph_id)
        account_types = account_types.rename(columns={'type': 'type_code'})

        result = self.graph.address_to_id.merge(account_types, how='left')
        result['type_code'] = result['type_code'].replace({0: 1, 1: 3}).fillna(0)

        # TODO what if a vertex NOT present in the account_type table is then found in type_labels? keep fake_incative

        frame = VertexMetadataService.merge_graph_vertices_with_metadata(graph_id, db)
        if not frame.empty:
            result = result.merge(frame, left_on='vertex', right_on='vertex', how='left')
            mark_labelled()
            result = result.groupby('vertex').first()
            result['type_code'] = result['type_code'].astype(np.int64)
            mark_token_icons()

        result['type_code'] = result['type_code'].replace(int_to_icon)

        print('\tGenerating vertices\' shapes took: ', time.monotonic() - start_time)

        return result.sort_values(['index'])['type_code'].values






