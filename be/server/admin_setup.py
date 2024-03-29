import os
import shutil

from flask import (
    Markup,
    flash,
)
from flask_admin.babel import gettext
from flask_admin.contrib.sqla import ModelView
from psycopg2._psycopg import AsIs

from be.configuration import (
    CONFIGURATIONS,
)

from sqlalchemy.sql import text

from be.server.gallery_categories import GalleryCategory
from be.server.gallery_categories.service import GalleryCategoryService
from be.server.graph import Graph


class GraphAdminView(ModelView):
    column_display_pk = True  # optional, but I like to see the IDs in the list
    column_hide_backrefs = False
    column_list = ('id', 'graph_name', 'vertices', 'edges', 'graph_category')

    def delete_model(self, graph):
        from be.server.server import app

        try:

            delete_vertex_edge_configs = """
            BEGIN;
                DROP TABLE :vertex_table;
                DROP TABLE :edge_table;
                DELETE FROM tg_graph_configs WHERE tg_graph_configs.graph = :graph_id;
                DELETE FROM tg_graphs WHERE tg_graphs.id = :graph_id;
            COMMIT;
            """
            self.session.execute(text(delete_vertex_edge_configs), {
                'graph_id': AsIs(graph.id),
                'vertex_table': AsIs(app.config['VERTEX_TABLE_NAME'](graph.id)),
                'edge_table': AsIs(app.config['EDGE_TABLE_NAME'](graph.id))
            })

        except Exception as e:
            flash(gettext('Failed to delete the graph: %(error)s', error=str(e)), 'error')
            return False

        try:
            shutil.rmtree(app.config['TILE_FOLDER_NAME'](graph.id))
        except Exception as e:
            flash(gettext('The graph was deleted in the db but the tiles deletion failed: %(error)s', error=str(e)),
                  'error')
            return False

        self.after_model_delete(graph)
        return True

    def _user_formatter(view, context, model, name):
        if model.graph_category:
            # from be.server.server import SessionLocal
            # with SessionLocal() as db:
            categories = GalleryCategoryService.get_all(view.session)
            category_title = next(filter(lambda cat: cat.id == model.graph_category, categories)).title
            markupstring = category_title
            return Markup(markupstring)
        else:
            return ""

    column_formatters = {
        'graph_category': _user_formatter
    }

class GraphCategoryView(ModelView):

    def delete_model(self, model):

        try:
            if len(self.session.query(Graph).filter_by(graph_category=model.id).all()) > 0:
                flash(gettext('Failed to delete. \n'
                              f'To delete this category ensure there are no graphs belonging to it'))
                return False
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

        # Model handlers

    def create_model(self, form):
        """
            Create model from form.

            :param form:
                Form instance
        """
        try:
            if form.data['urlslug'] == None or form.data['urlslug'] == '':
                raise Exception("URL slug needs to be populated")
            if ' ' in form.data['urlslug']:
                raise Exception("URL slug may not contain white spaces")
            model = self.build_new_instance()

            form.populate_obj(model)
            self.session.add(model)
            self._on_model_change(form, model, True)
            self.session.commit()
        except Exception as ex:
            if not self.handle_view_exception(ex):
                flash(gettext('Failed to create record. %(error)s', error=str(ex)), 'error')

            self.session.rollback()

            return False
        else:
            self.after_model_change(form, model, True)

        return model


def do_setup(admin, SessionLocal):
    admin.add_view(GraphCategoryView(GalleryCategory, SessionLocal()))
    admin.add_view(GraphAdminView(Graph, SessionLocal()))
