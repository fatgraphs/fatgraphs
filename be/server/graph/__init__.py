import os
import shutil

from flask import flash
from flask_admin.babel import gettext
from flask_admin.contrib.sqla import ModelView
from psycopg2._psycopg import AsIs

from .model import Graph  # noqa
from .schema import GraphSchema  # noqa
from .. import admin, SessionLocal
from ...configuration import VERTEX_TABLE_NAME, EDGE_TABLE_NAME, CONFIGURATIONS, TILE_FOLDER_NAME

BASE_ROUTE = "graph"


def register_routes(api, app):
    from .controller import api as user_api
    root = app.config['API_ROOT']
    api.add_namespace(user_api, path=f"/{root}/{BASE_ROUTE}")

    # make the graphs accessible via the flask admin interface

    class GraphAdminView(ModelView):
        column_display_pk = True  # optional, but I like to see the IDs in the list
        column_hide_backrefs = False
        column_list = ('id', 'graph_name', 'vertices', 'edges', 'graph_category')

        def delete_model(self, graph):

            try:

                delete_vertex_edge_configs = """
                BEGIN;
                    DROP TABLE %(vertex_table)s;
                    DROP TABLE %(edge_table)s;
                    DELETE FROM tg_graph_configs WHERE tg_graph_configs.graph = %(graph_id)s;
                    DELETE FROM tg_graphs WHERE tg_graphs.id = %(graph_id)s;
                COMMIT;
                """
                self.session.bind.engine.execute(delete_vertex_edge_configs, {
                    'graph_id': AsIs(graph.id),
                    'vertex_table': AsIs(VERTEX_TABLE_NAME(graph.id)),
                    'edge_table': AsIs(EDGE_TABLE_NAME(graph.id))
                })

            except Exception as e:
                flash(gettext('Failed to delete the graph: %(error)s', error=str(e)), 'error')
                return False

            try:
                shutil.rmtree(os.path.join(CONFIGURATIONS['graphsHome'], TILE_FOLDER_NAME(graph.id)))
            except Exception as e:
                flash(gettext('The graph was deleted in the db but the tiles deletion failed: %(error)s', error=str(e)), 'error')
                return False

            self.after_model_delete(graph)
            return True

    admin.add_view(GraphAdminView(Graph, SessionLocal()))
