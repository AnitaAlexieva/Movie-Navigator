from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.database import Base

class MovieList(Base):
    __tablename__ = "movie_lists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)

    # 🔗 Връзка с елементите в списъка
    items = relationship("MovieListItem", back_populates="list", cascade="all, delete-orphan")
