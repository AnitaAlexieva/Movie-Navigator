import httpx
import random
from models.movie import Movie
from dotenv import load_dotenv
import os

load_dotenv() 
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_API_URL = "https://api.themoviedb.org/3/discover/movie"

class MovieService:
    def __init__(self):
        self.client = httpx.AsyncClient()

    async def get_movies(self, genre: str = "", year: int = 0):
        params = {"api_key": TMDB_API_KEY}

        GENRES = {
        "action": 28,
        "comedy": 35,
        "horror": 27,
        "thriller": 53,
        "romance": 10749
    }
        if genre:
            genre_id = GENRES.get(genre.lower()) 
            if genre_id:
                params["with_genres"] = genre_id
                if year:
                    params["primary_release_year"] = year

        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(TMDB_API_URL, params=params)
            data = resp.json()
            movies = [
                Movie(
                    id=m["id"],
                    title=m["title"],
                    genre=genre or "N/A",
                    rating=m.get("vote_average", 0),
                    year=int(m.get("release_date", "2000")[:4]),
                    poster_url=f"https://image.tmdb.org/t/p/w500{m['poster_path']}" if m.get("poster_path") else None
                )
                for m in data.get("results", [])
            ]

            return movies
        except Exception as e:
            print(f"Error fetching movies: {e}")
            return []

    async def recommend_similar(self, movie: Movie):
        all_movies = await self.get_movies()
        if not all_movies:
            return []
        recommendations = random.sample(all_movies, min(3, len(all_movies)))
        return [m for m in recommendations if m.id != movie.id]

    async def get_movie_by_id(self, movie_id: int):
        """Взема конкретен филм по ID от TMDB API"""
        url = f"https://api.themoviedb.org/3/movie/{movie_id}"
        params = {"api_key": TMDB_API_KEY}

        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(url, params=params)

            if resp.status_code != 200:
                print(f"⚠️ TMDB API returned {resp.status_code} for movie ID {movie_id}")
                return None

            m = resp.json()
            return Movie(
                id=m["id"],
                title=m["title"],
                genre=", ".join([g["name"] for g in m.get("genres", [])]) or "N/A",
                rating=m.get("vote_average", 0),
                year=int(m.get("release_date", "2000")[:4]) if m.get("release_date") else 0,
                poster_url=f"https://image.tmdb.org/t/p/w500{m['poster_path']}" if m.get("poster_path") else None
            )

        except Exception as e:
            print(f"❌ Error fetching movie by ID {movie_id}: {e}")
            return None
