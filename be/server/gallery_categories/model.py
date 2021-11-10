from sqlalchemy import Integer, Column, String

from be.server import Base


class GalleryCategory(Base):

    __tablename__ = "gallery_categories"

    id = Column(Integer(), primary_key=True)
    title = Column(String())
    description = Column(String())
    freetext = Column(String())
    urlslug = Column(String())
