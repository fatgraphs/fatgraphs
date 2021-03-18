class Layout:

    def __init__(self, layout):
        self.max_x = layout['x'].max()
        self.max_y = layout['y'].max()
        self.min_x = layout['x'].min()
        self.min_y = layout['y'].min()
        self.width = self.max_x - self.min_x
        self.height = self.max_y - self.min_y
        self.vertex_id_to_xy_tuple = self._transform_layout(layout)

    def _transform_layout(self, layout):
        # vertex_first_cols = [layout.columns[-1]]
        # vertex_first_cols.extend(list(layout.columns[:-1]))
        # layout = layout[vertex_first_cols]
        # layout['xy'] = list(zip(layout['x'], layout['y']))
        # layout = layout.drop(['x', 'y'], axis=1)
        return layout
