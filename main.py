from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from controllers import movie_controller, list_controller
from database.init_db import init_db
from fastapi import Request
from fastapi.responses import HTMLResponse

app = FastAPI()

# Свържи папката за статични файлове (CSS, изображения)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/about", response_class=HTMLResponse)
def about_page(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})


# Определи къде се намират HTML шаблоните
templates = Jinja2Templates(directory="views")

# Включи контролера за филмите
app.include_router(movie_controller.router)
app.include_router(list_controller.router)

# Инициализация на базата данни при стартиране
@app.on_event("startup")
def startup_event():
    init_db()
