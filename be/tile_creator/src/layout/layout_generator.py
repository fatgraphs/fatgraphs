import cugraph
from cuml.neighbors import NearestNeighbors
import pandas as pd


class LayoutGenerator:

    def __init__(self):
        self.median_distance = -1
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
        self.median_distance = self._compute_median_distance(layout)
        layout = self._distribute_on_square_edges(layout)
        return layout

    def _compute_median_distance(self, layout):
        model = NearestNeighbors(n_neighbors=3)
        model.fit(layout[["x", "y"]].to_numpy())
        distances, indices = model.kneighbors(layout[["x", "y"]])
        return pd.DataFrame(distances).iloc[:, 1].median()

    def _distribute_on_square_edges(self, layout):
        def scale(array, a, b):
            return (b - a) * ((array - min(array)) / (max(array) - min(array))) + a

        # the layout is circular # to use more of the rectangular space, project onto a square
        u = layout["x"]
        v = layout["y"]
        umax = u.max()
        umin = u.min()
        vmax = v.max()
        vmin = v.min()
        sqrt = pd.np.sqrt

        # https://stats.stackexchange.com/a/178629

        u = scale(u, -0.9, 0.9)
        v = scale(v, -0.9, 0.9)

        # https://stackoverflow.com/a/32391780
        x = (0.5 * sqrt(2 + (u*u) - (v*v) + 2*u*sqrt(2))) - (0.5 * sqrt(2 + (u*u) - (v*v) - 2*u*sqrt(2)))
        y = (0.5 * sqrt(2 - (u*u) + (v*v) + 2*v*sqrt(2))) - (0.5 * sqrt(2 - (u*u) + (v*v) - 2*v*sqrt(2)))
        x = scale(x, umin, umax)
        y = scale(y, vmin, vmax)
        layout["x"] = x
        layout["y"] = y
        return layout

