from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from services.movie_service import MovieService
import random

templates = Jinja2Templates(directory="views")
router = APIRouter()
service = MovieService()

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/movies", response_class=HTMLResponse)
async def list_movies(request: Request, genre: str = "", year: int = 0):
    movies = await service.get_movies(genre, year)
    return templates.TemplateResponse("movies.html", {"request": request, "movies": movies})

@router.post("/recommendations", response_class=HTMLResponse)
async def recommendations(request: Request, movie_id: int = Form(...)):
    # Взимаме нов списък с филми (симулираме база)
    all_movies = await service.get_movies()

    # Опитваме да намерим избрания филм
    movie = next((m for m in all_movies if m.id == movie_id), None)
    if not movie and all_movies:
        movie = random.choice(all_movies)  # fallback ако не се намери

    # Симулираме "интелигентни" препоръки
    recs = await service.recommend_similar(movie)

    return templates.TemplateResponse(
        "recommendations.html",
        {
            "request": request,
            "recommendations": recs,
            "selected_movie": movie
        }
    )
@router.post("/lists/{list_id}/add_movie")
def add_movie(list_id: int, movie_id: int = Form(...)):
    item = service.add_movie_to_list(list_id, movie_id)
    if item:
        # Успешно добавен
        return {"status": "added"}
    else:
        # Вече е в списъка
        return {"status": "exists"}
