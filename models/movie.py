from pydantic import BaseModel

class Movie(BaseModel):
    id: int
    title: str
    genre: str
    rating: float
    year: int
    poster_url: str | None = None
