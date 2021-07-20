from typing import List

from flask import request
from flask_accepts import responds, accepts
from flask_restx import Namespace, Resource

from .model import Metadata, AUTOCOMPLETE_TERMS_PER_PAGE
from .schema import MetadataSchema, AutocompleteTermSchema
from .service import MetadataService
from .. import SessionLocal

api = Namespace("Metadata", description="Single namespace, single entity")  # noqa

@api.route("/vertex/<string:eth>")
@api.param("eth", "Ethereum address")
class MetadataEthResource(Resource):

    @responds(schema=MetadataSchema(many=True))
    def get(self, eth: str) -> List[Metadata]:
        with SessionLocal() as db:
            by_eth = MetadataService.get_by_eth(eth, db)
            return by_eth

@api.route("/create")
class MetadataResource(Resource):

    @accepts(schema=MetadataSchema, api=api)
    @responds(schema=MetadataSchema)
    def post(self) -> Metadata:
        with SessionLocal() as db:
            by_eth = MetadataService.create(request.parsed_obj, db)
            return by_eth


@api.route("/autocomplete-term/<int:page>")
@api.param("page", f"Page for pagination, {AUTOCOMPLETE_TERMS_PER_PAGE} per page")
class AutocompleteTermsResource(Resource):

    # tis annotation automatically casts the Metadata item to AutocompleteTermSchema
    @responds(schema=AutocompleteTermSchema(many=True))
    def get(self, page: int) -> List[Metadata]:
        with SessionLocal() as db:
            autocomplete_terms = MetadataService.get_autocomplete_term(page, db)
            return autocomplete_terms
