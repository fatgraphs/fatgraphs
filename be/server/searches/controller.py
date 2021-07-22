from typing import List

from flask import request
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource

from . import SearchTerm, AUTOCOMPLETE_TERMS_PER_PAGE
from .schema import SearchTermSchema
from .service import SearchTermService
from .. import SessionLocal

api = Namespace("Searches", description="Search terms that can be used while exploring the graph")  # noqa


@api.route("/")
class RecentSearchTermsResource(Resource):

    @responds(schema=SearchTermSchema(many=True))
    def get(self) -> SearchTermSchema:
        with SessionLocal() as db:
            objects = SearchTermService.get_recent_searches(db)
            return objects

    @accepts(schema=SearchTermSchema, api=api)
    @responds(schema=SearchTermSchema(many=True))
    def put(self) -> List[SearchTerm]:
        with SessionLocal() as db:
            terms = SearchTermService.update_search_terms(request.parsed_obj, db)
            return terms


@api.route("/autocomplete-term/<int:page>")
@api.param("page", f"Page for pagination, {AUTOCOMPLETE_TERMS_PER_PAGE} per page")
class AutocompleteTermsResource(Resource):

    # tis annotation automatically casts the Metadata item to AutocompleteTermSchema
    @responds(schema=SearchTermSchema(many=True))
    def get(self, page: int) -> List[SearchTerm]:
        with SessionLocal() as db:
            terms = SearchTermService.get_autocomplete_terms(page, db)
            return terms
