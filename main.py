from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from controllers import movie_controller

app = FastAPI()

# 1️⃣ Свържи папката "static"
app.mount("/static", StaticFiles(directory="static"), name="static")

# 2️⃣ Кажи на FastAPI къде са шаблоните
templates = Jinja2Templates(directory="views")

# 3️⃣ Добави контролера
app.include_router(movie_controller.router)
