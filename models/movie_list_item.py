from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base

class MovieListItem(Base):
    __tablename__ = "movie_list_items"

    movie_id = Column(Integer, primary_key=True)
    list_id = Column(Integer, ForeignKey("movie_lists.id"), primary_key=True)

    # 🔗 Релация към MovieList
    list = relationship("MovieList", back_populates="items")
