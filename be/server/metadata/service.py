from typing import List

from .interface import MetadataInterface
from .model import Metadata, AUTOCOMPLETE_TERMS_PER_PAGE


class MetadataService:

    @staticmethod
    def get_by_eth(eth: str, db: object) -> List[Metadata]:
        metadatas = db.query(Metadata).filter_by(eth_source=eth).all()
        return metadatas

    @staticmethod
    def get_by_type_and_value(meta_type: str, meta_value: str, db: object) -> List[Metadata]:
        matches = db.query(Metadata).filter_by(meta_type=meta_type, meta_value=meta_value).all()
        return matches

    @staticmethod
    def get_autocomplete_term(page: int, db: object) -> List[Metadata]:
        unique_terms = db.query(Metadata)\
            .distinct(Metadata.meta_value)\
            .offset(page * AUTOCOMPLETE_TERMS_PER_PAGE)\
            .limit(AUTOCOMPLETE_TERMS_PER_PAGE).all()
        return unique_terms

    @staticmethod
    def create(metadata_to_insert: MetadataInterface, db: object):

        new_metadata = Metadata(
            eth_source=metadata_to_insert['eth_source'],
            eth_target=getattr(metadata_to_insert, 'eth_target', ""),
            meta_type=metadata_to_insert['meta_type'],
            meta_value=metadata_to_insert['meta_value'],
            entity=metadata_to_insert['entity'])

        db.add(new_metadata)
        db.commit()
        return new_metadata

    @staticmethod
    def assemble_recent_searches(user):
        two_arrays = user.recent_metadata_searches
        mt = list(zip(['meta_type'] * 5, two_arrays[1]))
        mv = list(zip(['meta_value'] * 5, two_arrays[0]))
        zipped = list(zip(mt, mv))
        dictionary = list(map(lambda e: dict(e), zipped))
        return dictionary
