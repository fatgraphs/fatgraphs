from flask import flash
from flask_admin.babel import gettext
from flask_admin.contrib.sqla import ModelView
from psycopg2._psycopg import AsIs

from .model import Graph  # noqa
from .schema import GraphSchema  # noqa
from .. import admin, SessionLocal
from ...configuration import VERTEX_TABLE_NAME, EDGE_TABLE_NAME

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

        def delete_model(self, model):

            try:

                delte_vertex_table = """DROP TABLE %(table_name)s;"""

                result = self.session.bind.engine.execute(delte_vertex_table, {
                    'table_name': AsIs(VERTEX_TABLE_NAME(model.id)),
                })

                delte_edge_table = """DROP TABLE %(table_name)s;"""

                result = self.session.bind.engine.execute(delte_edge_table, {
                    'table_name': AsIs(EDGE_TABLE_NAME(model.id)),
                })

                delete_configuration_entry = """DELETE FROM tg_graph_configs WHERE tg_graph_configs.graph = %(graph_id)s;"""

                result = self.session.bind.engine.execute(delete_configuration_entry, {
                    'graph_id': model.id,
                })

                self.on_model_delete(model)
                self.session.flush()
                self.session.delete(model)
                self.session.commit()
            except Exception as ex:
                if not self.handle_view_exception(ex):
                    flash(gettext('Failed to delete record. %(error)s', error=str(ex)), 'error')

                self.session.rollback()

                return False
            else:
                self.after_model_delete(model)

            return True

    admin.add_view(GraphAdminView(Graph, SessionLocal()))


