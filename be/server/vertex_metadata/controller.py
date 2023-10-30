import json
from typing import List

from flask import (
    Response,
    request,
)
from flask_accepts import (
    accepts,
    responds,
)
from flask_restx import (
    Namespace,
    Resource,
)

from be.server.server import SessionLocal

from be.server.vertex_metadata import VertexMetadataSchema
from be.server.vertex_metadata.model import VertexMetadata
from be.server.vertex_metadata.service import VertexMetadataService
from be.server.server import app

api = Namespace("VertexMetadata", description="Global metadata related to eth addresses")

@api.route("/<int:graph_id>")
@api.param("graph_id")
class MetadataVerticesGraphResource(Resource):

    @responds(schema=VertexMetadataSchema(many=True))
    def get(self, graph_id: int) -> List[VertexMetadata]:

        def stream(t: List):
            for row in t:
                yield json.dumps(row) + "\n"

        with SessionLocal() as db:
            vertex_metadatas = VertexMetadataService.get_all_by_graph(graph_id, db)
            vertex_metadatas = [e.as_dict() for e in vertex_metadatas]
            return Response(stream(vertex_metadatas))

@api.route("/vertex/<string:eth>")
@api.param("eth", "Ethereum address")
class MetadataEthResource(Resource):

    @responds(schema=VertexMetadataSchema(many=True))
    def get(self, eth: str) -> List[VertexMetadata]:
        with SessionLocal() as db:
            by_eth = VertexMetadataService.get_by_vertex(eth, db)
            return by_eth

@api.route("/create")
class MetadataResource(Resource):

    @accepts(schema=VertexMetadataSchema, api=api)
    @responds(schema=VertexMetadataSchema)
    def post(self) -> VertexMetadata:
        if not app.config['IS_LABELLING_ENABLED']:
            print("\tLabelling is disabled in config, this endpoint is not active")
            return {}
        with SessionLocal() as db:
            by_eth = VertexMetadataService.create(request.parsed_obj, db)
            return by_eth


@api.route("/<string:vertex_ext_id>")
@api.param("vertex_type")
@api.param("vertex_label")
class MetadataResource(Resource):

    @responds(schema=VertexMetadataSchema)
    def delete(self, vertex_ext_id: str) -> VertexMetadata:
        if not app.config['IS_LABELLING_ENABLED']:
            return Response(
                "Labelling is disabled in config, this endpoint is not active",
                400,
            )
        
        vertex_type = request.args.get('vertex_type', None)
        vertex_label = request.args.get('vertex_label', None)
        
        if vertex_type is None and vertex_label is None:
            return Response(
                "For security you need to provide type or label, deleting all Metadatas for the vertex should be its own endpoint",
                400
            )
        with SessionLocal() as db:
            query = db.query(VertexMetadata).filter(VertexMetadata.vertex == vertex_ext_id)

        if vertex_type is not None:
            query = query.filter(VertexMetadata.type == vertex_type)

        if vertex_label is not None:
            query = query.filter(VertexMetadata.label == vertex_label)

        count = query.delete()
        db.commit()
        return Response(f"Deleted {count} Metadatas for {vertex_ext_id}")
