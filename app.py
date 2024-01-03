from fastapi import FastAPI
from core.routes import router
from core.routers.auth import router as auth_router

app = FastAPI()
app.include_router(router)
app.include_router(auth_router)
