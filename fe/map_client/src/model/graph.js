class Graph {

    constructor(rawGraph) {
        this.tileSize = rawGraph.tileSize
        this.maxTransparency = rawGraph.maxTransparency
        this.medianPixelDistance = rawGraph.medianPixelDistance
        this.max = rawGraph.max
        this.vertices = rawGraph.vertices
        this.bgColor = rawGraph.bgColor
        this.medVertexSize = rawGraph.medVertexSize
        this.maxVertexSize = rawGraph.maxVertexSize
        this.curvature = rawGraph.curvature
        this.minTransparency = rawGraph.minTransparency
        this.source = rawGraph.source
        this.edges = rawGraph.edges
        this.stdTransparencyAsPercentage = rawGraph.stdTransparencyAsPercentage
        this.min = rawGraph.min
        this.zoomLevels = rawGraph.zoomLevels
        this.outputFolder = rawGraph.outputFolder
        this.tileBasedMeanTransparency = rawGraph.tileBasedMeanTransparency
        this.medEdgeThickness = rawGraph.medEdgeThickness
        this.id = rawGraph.id
        this.graphName = rawGraph.graphName
        this.maxEdgeThickness = rawGraph.maxEdgeThickness
        this.labels = rawGraph.labels

    }

}

export default Graph;

