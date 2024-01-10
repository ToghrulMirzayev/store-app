from sqladmin import ModelView
from core.models import User, Store, Product


class UserAdmin(ModelView, model=User):
    icon = "fa-solid fa-user"
    column_list = [User.username, User.email]
    can_delete = False
    can_edit = False
    column_details_exclude_list = [User.hashed_password]


class StoreAdmin(ModelView, model=Store):
    icon = "fa-solid fa-store"
    column_list = [Store.store_name, Store.location, Store.address]
    can_delete = False
    can_edit = False


class ProductAdmin(ModelView, model=Product):
    icon = "fa-solid fa-object-group"
    column_list = [Product.product_name, Product.store_id]
    can_delete = False
    can_edit = False
