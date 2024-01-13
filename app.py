from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqladmin import Admin
from sqlalchemy.orm import joinedload
from core.models import Store
from core.routers.stores import router as store_router
from core.routers.products import router as product_router
from core.routers.auth import router as auth_router
from env_config import engine, SessionLocal
from core.admin_panel import UserAdmin, StoreAdmin, ProductAdmin

app = FastAPI(
    version='1.0.0',
    title='Store Application'
)
app.include_router(store_router)
app.include_router(product_router)
app.include_router(auth_router)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def render_template(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/stores")
async def render_stores(request: Request):
    with SessionLocal() as session:
        stores = session.query(Store).options(joinedload(Store.products)).all()
    return templates.TemplateResponse("stores.html", {"request": request, "stores": stores})


admin = Admin(app, engine)

admin.add_view(UserAdmin)
admin.add_view(StoreAdmin)
admin.add_view(ProductAdmin)
