import pandas as pd


class TokenGraphMetadata:

    def __init__(self, tokenGraph, layout, configurationDictionary):
        self.configurations = None
        self.graphData = None

        configurationDictionary['labels'] = "" if configurationDictionary['labels'] is None else \
            configurationDictionary['labels']
        self.configurations = pd.DataFrame(data=configurationDictionary, index=[0])

        self.graphData = pd.DataFrame(data={
            'median_pixel_distance': layout.medianPixelDistance,
            'min': layout.min,
            'max': layout.max,
            'vertices': [tokenGraph.addressToId.shape[0]],
            'edges': [tokenGraph.edgeIdsToAmount.shape[0]]})

    def getGraphName(self):
        return self.configurations['graph_name'][0]

    def getZoomLevels(self):
        return self.configurations['zoom_levels'][0]

    def getMinCoordinate(self):
        return self.graphData['min'][0]

    def getMaxCoordinate(self):
        return self.graphData['max'][0]

    def getSingleFrame(self):
        return pd.concat([self.configurations, self.graphData], axis=1)
