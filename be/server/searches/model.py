from sqlalchemy import Integer, Column, String
from be.server import Base


class SearchTerm(Base):
    __tablename__ = "tg_search"

    id = Column(Integer, primary_key=True)
    type = Column(String)
    value = Column(String)