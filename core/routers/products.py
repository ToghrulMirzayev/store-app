from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi import status
from core.schemas import ProductCreate, ProductResponse
from core.models import Product as ProductDB
from env_config import SessionLocal
from core.routers.auth import get_current_user, get_user_exception

router = APIRouter(
    prefix='/product',
    tags=['product']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/create-product", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(product_create: ProductCreate,
                         user: dict = Depends(get_current_user),
                         db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    product_data = product_create.model_dump()
    if "product_id" not in product_data:
        product_data["product_id"] = (lambda existing_ids: 1 if not existing_ids else max(existing_ids) + 1)(
            [product.product_id for product in db.query(ProductDB).all()]
        )
    db_product = ProductDB(**product_data)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@router.get("/get-product/{product_id}", response_model=ProductResponse)
async def read_product(product_id: int,
                       user: dict = Depends(get_current_user),
                       db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    db_product = db.query(ProductDB).filter(ProductDB.product_id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@router.get("/get-products", response_model=List[ProductResponse])
async def read_products(skip: int = 0, limit: int = 10,
                        user: dict = Depends(get_current_user),
                        db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    products = db.query(ProductDB).offset(skip).limit(limit).all()
    return products


@router.delete("/delete-product/{product_id}", response_model=None)
async def delete_product(product_id: int,
                         user: dict = Depends(get_current_user),
                         db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    db_product = db.query(ProductDB).filter(ProductDB.product_id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()


@router.patch("/update-product-availability/{product_id}", response_model=None)
async def update_product_availability(product_id: int,
                                      is_available: bool,
                                      user: dict = Depends(get_current_user),
                                      db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    if user['role'] != 'admin':
        raise HTTPException(status_code=403, detail="Permission denied. Only admins can update product availability "
                                                    "manually")
    db_product = db.query(ProductDB).filter(ProductDB.product_id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db_product.is_available = is_available
    db.commit()
