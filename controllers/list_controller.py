from fastapi import APIRouter, Form, Request,Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from services.list_service import ListService
from services.movie_service import MovieService
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from models.movie_list import MovieList
from models.movie_list_item import MovieListItem
from database.database import get_db


router = APIRouter()
templates = Jinja2Templates(directory="views")
service = ListService()
movie_service = MovieService()

# 📄 Показване на всички персонални списъци
@router.get("/lists")
def show_lists(request: Request):
    lists = service.get_all_lists()
    return templates.TemplateResponse("lists.html", {"request": request, "lists": lists})

# ➕ Добавяне на нов списък
@router.post("/lists/create")
def create_list(name: str = Form(...), description: str = Form(None)):
    service.create_list(name=name, description=description)
    return RedirectResponse(url="/lists", status_code=303)

# ❌ Изтриване на списък
@router.post("/lists/delete/{list_id}")
def delete_list(list_id: int):
    service.delete_list(list_id)
    return RedirectResponse(url="/lists", status_code=303)

# ➕ Добавяне на филм към списък
@router.post("/lists/{list_id}/add_movie")
def add_movie(list_id: int, movie_id: int = Form(...)):
    service.add_movie_to_list(list_id, movie_id)
    return RedirectResponse(url=f"/lists/{list_id}", status_code=303)

# ➕ Добавяне на филм към списък (JSON отговор за модала)
@router.post("/lists/{list_id}/add_movie/json")
def add_movie_json(list_id: int, movie_id: int = Form(...)):
    try:
        item = service.add_movie_to_list(list_id, movie_id)
        if item:
            return JSONResponse({"status": "added"})
        else:
            return JSONResponse({"status": "exists"})
    except Exception as e:
        # Връщаме JSON с грешката, за да не се счупи JS fetch
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)


# Връща всички списъци като JSON
@router.get("/lists/json")
def lists_json():
    lists = service.get_all_lists()
    return JSONResponse([{"id": l.id, "name": l.name} for l in lists])

# Създаване на нов списък през JSON
@router.post("/lists/create/json")
async def create_list_json(request: Request):
    payload = await request.json()   # прочитаме JSON body
    name = payload.get("name")
    description = payload.get("description")
    new_list = service.create_list(name, description)
    return JSONResponse({"id": new_list.id, "name": new_list.name})

# 📄 Показване на конкретен списък и неговите филми
@router.get("/lists/{list_id}")
async def show_list(list_id: int, request: Request):
    movie_list = service.get_list_by_id(list_id)  # връща MovieList с name, description
    movie_ids = service.get_movies_in_list(list_id)
    movies = [await movie_service.get_movie_by_id(mid) for mid in movie_ids]
    return templates.TemplateResponse(
        "list_detail.html",
        {"request": request, "movie_list": movie_list, "movies": movies}  # ключът е movie_list
    )

@router.post("/lists/{list_id}/remove_movie/json")
async def remove_movie_from_list(list_id: int, request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    movie_id = int(form.get("movie_id"))

    # Проверка дали списъкът съществува
    list_obj = db.query(MovieList).filter(MovieList.id == list_id).first()
    if not list_obj:
        return JSONResponse({"status": "error", "message": "List not found"})

    # Търсим съответния елемент
    item = db.query(MovieListItem).filter(
        MovieListItem.list_id == list_id,
        MovieListItem.movie_id == movie_id
    ).first()

    if item:
        db.delete(item)
        db.commit()
        return JSONResponse({"status": "removed"})
    else:
        return JSONResponse({"status": "not_found"})
