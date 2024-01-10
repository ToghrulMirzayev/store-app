from fastapi import FastAPI
from sqladmin import Admin
from core.routers.stores import router as store_router
from core.routers.products import router as product_router
from core.routers.auth import router as auth_router
from env_config import engine
from core.admin_panel import UserAdmin, StoreAdmin, ProductAdmin

app = FastAPI(
    version='1.0.0',
    title='Store Application'
)
app.include_router(store_router)
app.include_router(product_router)
app.include_router(auth_router)


admin = Admin(app, engine)

admin.add_view(UserAdmin)
admin.add_view(StoreAdmin)
admin.add_view(ProductAdmin)
