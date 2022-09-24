from typing import List

from flask_accepts import responds
from flask_restx import Namespace, Resource

from . import SearchTerm
from .schema import SearchTermSchema
from .service import SearchTermService
from .. import SessionLocal

api = Namespace("Searches", description="Search terms that can be used while exploring the graph")  # noqa


@api.route("/autocomplete-term/<int:graph_id>")
@api.param("graph_id", "The graph id")
class AutocompleteTermsResource(Resource):

    # tis annotation automatically casts the Metadata item to AutocompleteTermSchema
    @responds(schema=SearchTermSchema(many=True))
    def get(self, graph_id: int) -> List[SearchTerm]:
        with SessionLocal() as db:
            terms = SearchTermService.get_autocomplete_terms(graph_id, db)
            return terms
