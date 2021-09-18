import pandas as pd


class TokenGraphMetadata:

    def __init__(self, tokenGraph, layout, configurationDictionary):
        self.configurations = None
        self.graphData = None

        self.configurations = pd.DataFrame(data=configurationDictionary, index=[0])

        self.graphData = pd.DataFrame(data={
            'median_pixel_distance': layout.medianPixelDistance,
            'min': layout.min,
            'max': layout.max,
            'vertices': [tokenGraph.address_to_id.shape[0]],
            'edges': [tokenGraph.edge_ids_to_amount.shape[0]]})

    def get_config_dict(self):
        frame = self._get_single_frame()
        return frame.to_dict(orient='record')[0]

    def getGraphName(self):
        return self.configurations['graph_name'][0]

    def getZoomLevels(self):
        return self.configurations['zoom_levels'][0]

    def getMinCoordinate(self):
        return self.graphData['min'][0]

    def getMaxCoordinate(self):
        return self.graphData['max'][0]

    def _get_single_frame(self):
        return pd.concat([self.configurations, self.graphData], axis=1)
