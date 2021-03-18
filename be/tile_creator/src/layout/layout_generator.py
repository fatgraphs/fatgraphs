import cugraph

from be.tile_creator.src.layout.layout import Layout


class LayoutGenerator:

    def __init__(self):
        self.default_force_atlas_2_options = {'max_iter': 500,
                                              'strong_gravity_mode': True,
                                              'barnes_hut_theta': 1.2,
                                              'outbound_attraction_distribution': False,
                                              'gravity': 1,
                                              'scaling_ratio': 1}

    def make_layout(self, data):
        # so far there is only one way of generating a layout, if needed implement strategy pattern
        return self._run_force_atlas_2(data)

    def _run_force_atlas_2(self, gpu_graph):
        if not isinstance(gpu_graph, cugraph.structure.graph.Graph):
            raise TypeError("The cuGraph implementation of Force Atlas requires a gpu frame")
        # layout: x y vertex
        layout = cugraph.layout.force_atlas2(gpu_graph, **self.default_force_atlas_2_options)
        layout = layout.to_pandas()
        return Layout(layout)


