from fastapi import FastAPI
from core.routes import router

app = FastAPI()
app.include_router(router)
