from fastapi import FastAPI
from core.routers.stores import router as store_router
from core.routers.products import router as product_router
from core.routers.auth import router as auth_router

app = FastAPI(
    version='1.0.0',
    title='Store Application'
)
app.include_router(store_router)
app.include_router(product_router)
app.include_router(auth_router)
