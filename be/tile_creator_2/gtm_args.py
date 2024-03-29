class GtmArgs():

    def __init__(self, configurations: dict):
        self.configurations = configurations

    def get_name(self):
        return self.configurations["graph_name"]

    def get_tile_size(self):
        return self.configurations["tile_size"]

    def get_median_edge_thickness(self):
        # return config['med_edge_thickness']
        return self.configurations["med_edge_thickness"]

    def get_max_edge_thickness(self):
        # config['max_edge_thickness']
        return self.configurations["max_edge_thickness"]

    def get_zoom_levels(self):
        return self.configurations["zoom_levels"]

    def get_std_percentage(self):
        return self.configurations["std_transparency_as_percentage"]

    def get_tile_based_mean_transparency(self):
        return self.configurations["tile_based_mean_transparency"]

    def get_min_transparency(self):
        return self.configurations["min_transparency"]

    def get_max_transparency(self):
        return self.configurations["max_transparency"]

    def get_max_vertex_size(self):
        return self.configurations["max_vertex_size"]

    def get_med_vertex_size(self):
        return self.configurations["med_vertex_size"]

    def get_category(self):
        return self.configurations["graph_category"]

    def get_curvature(self):
        return self.configurations["curvature"]

    def get_bg_color(self):
        return self.configurations["bg_color"]

    def get_source_file(self):
        return self.configurations["source"]

    def get_description(self):
        return self.configurations['description']

    def to_json_camel_case(self, graph_data, graph_id):
        return dict(
            tileSize=self.get_tile_size(),
            zoomLevels=self.get_zoom_levels(),
            minTransparency=float(self.get_min_transparency()),
            maxTransparency=float(self.get_max_transparency()),
            tileBasedMeanTransparency=float(self.get_tile_based_mean_transparency()),
            stdTransparencyAsPercentage=float(self.get_std_percentage()),
            maxEdgeThickness=float(self.get_max_edge_thickness()),
            medEdgeThickness=float(self.get_median_edge_thickness()),
            maxVertexSize=float(self.get_max_vertex_size()),
            medVertexSize=float(self.get_med_vertex_size()),
            curvature=float(self.get_curvature()),
            bgColor=self.get_bg_color(),
            source=self.get_source_file(),

            #TODO remove and put in graph data
            medianPixelDistance=float(graph_data.median_pixel_distance),
            min=float(graph_data.graph_space_bound.get_min_coord()),
            max=float(graph_data.graph_space_bound.get_max_coord()),

            graph=graph_id,
        )


