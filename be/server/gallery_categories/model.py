from sqlalchemy import Integer, Column, String
from sqlalchemy.orm import relationship

from be.server import Base


class GalleryCategory(Base):

    __tablename__ = "gallery_categories"

    id = Column(Integer(), primary_key=True)
    title = Column(String())
    description = Column(String())
    freetext = Column(String())
    urlslug = Column(String())
    graph = relationship('Graph', backref='galleryCategory', lazy='dynamic')

    def __str__(self):
        return self.title
