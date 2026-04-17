from fastapi import FastAPI
from app.controllers.files_controller import router

app = FastAPI()
app.include_router(router)