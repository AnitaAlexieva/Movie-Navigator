from fastapi import FastAPI
from controllers import movie_controller

app = FastAPI()
app.include_router(movie_controller.router)
