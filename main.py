from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from controllers import movie_controller, list_controller
from database.init_db import init_db

app = FastAPI()

# Свържи папката за статични файлове (CSS, изображения)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Определи къде се намират HTML шаблоните
templates = Jinja2Templates(directory="views")

# Включи контролера за филмите
app.include_router(movie_controller.router)
app.include_router(list_controller.router)

# Инициализация на базата данни при стартиране
@app.on_event("startup")
def startup_event():
    init_db()
