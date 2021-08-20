from graph_tool import Graph
import numpy as np

class GraphToolTokenGraph:
    '''
    This contains a token graph that is specifically used with the library graph_tool.
    An instacne of GraphToolTokenGraph contains all the static information needed to render a graph.
    '''

    def __init__(self, edgeIdsToAmount, visualLayout, metadata, edgeCurvature):
        self.metadata = metadata
        self.edgeCurvature = edgeCurvature if edgeCurvature < 0 else -1 * edgeCurvature
        self.g = Graph(directed=True)
        self.addEdges(edgeIdsToAmount)
        self.vertexPositions = self.g.new_vertex_property("vector<float>",
                                                      vals=visualLayout.vertexPositions[["x", "y"]].values)
        self.edgeLength = self.g.new_edge_property("float", vals=visualLayout.edgeLengths)
        self.vertexSizes = self.g.new_vertex_property('float', vals=visualLayout.vertexSizes)
        self.vertexShapes = self.g.new_vertex_property('string', vals=visualLayout.vertexShapes)
        self.edgeThickness = self.g.new_edge_property("float", vals=visualLayout.edgeThickness)
        self.makeBezierPoints()
        # edge transparency needs to be populated at run-time
        self.edgeTransparencies = []
        rgba = [[1.0] * len(visualLayout.edgeTransparencies[0])] * 4

        for zl in range(0, metadata.getZoomLevels()):
            self.edgeTransparencies.append(self.g.new_edge_property("vector<float>"))
            rgba[3] = list(visualLayout.edgeTransparencies[zl].to_numpy()) # set alpha based on zoom
            self.edgeTransparencies[zl].set_2d_array(np.array(rgba))

    def makeBezierPoints(self):
        self.controlPoints = self.g.new_edge_property('vector<float>')
        for v in self.g.vertices():
            for e in v.out_edges():
                curvature = self.edgeLength[e] * self.edgeCurvature
                self.controlPoints[e] = [0, 0, 0.25, curvature, 0.75, curvature, 1, 0]

    def addEdges(self, edgeIdsToAmount):
        data = edgeIdsToAmount.rename(columns={'sourceId': 'source', 'targetId': 'target'})
        # hashed = False ensure that vertex values correspond to vertex indices
        self.g.add_edge_list(
            data[["source", "target"]].values,
            hashed=False)
