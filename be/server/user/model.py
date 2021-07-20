from sqlalchemy import Integer, Column, String
from sqlalchemy.dialects.postgresql import ARRAY
from be.server import Base


class User(Base):
    __tablename__ = "tg_user"

    name = Column(String(255), primary_key=True)
    recent_metadata_searches = Column(ARRAY(String(255)))