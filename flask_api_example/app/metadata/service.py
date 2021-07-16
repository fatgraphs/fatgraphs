from app import db
from typing import List

from .interface import MetadataInterface
from .model import Metadata, AUTOCOMPLETE_TERMS_PER_PAGE


class MetadataService:

    @staticmethod
    def get_by_eth(eth: str) -> List[Metadata]:
        eth__all = Metadata.query.filter_by(eth_source=eth).all()
        return eth__all

    @staticmethod
    def get_by_type_and_value(meta_type: str, meta_value: str) -> List[Metadata]:
        eth__all = Metadata.query.filter_by(meta_type=meta_type, meta_value=meta_value).all()
        return eth__all

    @staticmethod
    def get_autocomplete_term(page: int) -> List[Metadata]:
        metas = Metadata.query.distinct(Metadata.meta_value).paginate(page, AUTOCOMPLETE_TERMS_PER_PAGE, True).items
        return metas

    @staticmethod
    def create(metadata_to_insert: MetadataInterface):
        new_metadata = Metadata(
            eth_target=metadata_to_insert['eth_target'],
            eth_source=metadata_to_insert['eth_source'],
            meta_type=metadata_to_insert['meta_type'],
            meta_value=metadata_to_insert['meta_value'],
            entity=metadata_to_insert['entity'])

        db.session.add(new_metadata)
        db.session.commit()
        return new_metadata
