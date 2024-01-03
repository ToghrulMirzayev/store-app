from typing import List
from pydantic import BaseModel


class Product:
    def __init__(self, product_name: str, is_available: bool, store_id: int, product_id: int = None):
        self.product_id = product_id
        self.product_name = product_name
        self.is_available = is_available
        self.store_id = store_id


class Store:
    def __init__(self, location: str, store_name: str, store_id: int = None):
        self.store_id = store_id
        self.store_name = store_name
        self.location = location
        self.products = []


class ProductResponse(BaseModel):
    product_id: int
    product_name: str
    is_available: bool
    store_id: int


class StoreResponse(BaseModel):
    location: str
    store_name: str
    products: List[ProductResponse]


class ProductCreate(BaseModel):
    product_name: str
    is_available: bool
    store_id: int


class StoreCreate(BaseModel):
    location: str
    store_name: str


class UserRegister(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
