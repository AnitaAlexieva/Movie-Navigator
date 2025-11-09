# database/init_db.py
from database.database import Base, engine
from models.movie_list_item import MovieListItem
from models.movie_list import MovieList
from models.movie import Movie


def init_db():
    # Това ще създаде всички таблици, които са импортирани от Base
    Base.metadata.create_all(bind=engine)
