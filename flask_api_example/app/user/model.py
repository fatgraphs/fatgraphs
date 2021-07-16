from sqlalchemy import Integer, Column, String
from app import db  # noqa
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship

from .interface import UserInterface


class User(db.Model):
    __tablename__ = "tg_user"

    name = Column(String(255), primary_key=True)
    recent_metadata_searches = Column(ARRAY(String(255)))
    graphs = relationship("Graph")

    # @staticmethod
    # def update_search_terms(new_term: str, user: User):
    #     recent_metadata_searches = user.recent_metadata_searches #getattr(self, "recent_metadata_searches")
    #     recent_metadata_searches.insert(0, new_term)
    #     user.recent_metadata_searches = recent_metadata_searches #setattr(self, "recent_metadata_searches", recent_metadata_searches[0:5]
