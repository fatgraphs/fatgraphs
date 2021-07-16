from app import db  # noqa
from sqlalchemy import Column, String, Integer


class Metadata(db.Model):
    __tablename__ = "tg_metadata"

    id = Column(Integer(), primary_key=True)
    eth_target = Column(String())
    eth_source = Column(String())
    meta_type = Column(String())
    meta_value = Column(String())
    entity = Column(String())


AUTOCOMPLETE_TERMS_PER_PAGE = 100
