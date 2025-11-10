from database.database import SessionLocal
from models.movie_list import MovieList
from models.movie_list_item import MovieListItem

class ListService:
    def get_all_lists(self):
        with SessionLocal() as db:
            return db.query(MovieList).all()

    def create_list(self, name: str, description: str | None = None):
        with SessionLocal() as db:
            new_list = MovieList(name=name, description=description)
            db.add(new_list)
            db.commit()
            db.refresh(new_list)
            return new_list

    def delete_list(self, list_id: int):
        with SessionLocal() as db:
            movie_list = db.query(MovieList).filter(MovieList.id == list_id).first()
            if movie_list:
                db.delete(movie_list)
                db.commit()
                return True
            return False
        
    def add_movie_to_list(self, list_id: int, movie_id: int):
        with SessionLocal() as db:
            print("Добавям филм", movie_id, "в списък", list_id)
            movie_list = db.query(MovieList).filter(MovieList.id == list_id).first()
            if not movie_list:
                print("Списъкът не съществува!")
                raise ValueError(f"List with id {list_id} does not exist")
            
            exists = db.query(MovieListItem).filter_by(list_id=list_id, movie_id=movie_id).first()
            if not exists:
                item = MovieListItem(list_id=list_id, movie_id=movie_id)
                db.add(item)
                db.commit()
                db.refresh(item)
                print("Филм добавен:", item)
                return item
            print("Филмът вече е в списъка")
            return None


    def get_movies_in_list(self, list_id: int):
        with SessionLocal() as db:
            items = db.query(MovieListItem).filter_by(list_id=list_id).all()
            return [item.movie_id for item in items]

    def get_list_by_id(self, list_id: int):
        with SessionLocal() as db:
            return db.query(MovieList).filter(MovieList.id == list_id).first()
