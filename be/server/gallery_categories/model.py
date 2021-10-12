from sqlalchemy import Integer, Column, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from be.server import Base
from be.server.graph.interface import GraphInterface


class GalleryCategory(Base):

    __tablename__ = "gallery_categories"

    id = Column(Integer(), primary_key=True)
    title = Column(String())
    description = Column(String())
    freetext = Column(String())
    urlslug = Column(String())
