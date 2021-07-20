from sqlalchemy import Column, String, Integer

from be.server import Base


class Metadata(Base):
    __tablename__ = "tg_metadata"

    id = Column(Integer(), primary_key=True)
    eth_target = Column(String())
    eth_source = Column(String())
    meta_type = Column(String())
    meta_value = Column(String())
    entity = Column(String())


AUTOCOMPLETE_TERMS_PER_PAGE = 200
