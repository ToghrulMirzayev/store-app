from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi import status
from core.models import StoreResponse, StoreCreate, ProductCreate, ProductResponse
from core.db_models import Store as StoreDB, Product as ProductDB
from env_config import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/store", response_model=StoreResponse, status_code=status.HTTP_201_CREATED)
async def create_store(store_create: StoreCreate, db: Session = Depends(get_db)):
    store_data = store_create.model_dump()
    if "store_id" not in store_data:
        store_data["store_id"] = (lambda existing_ids: 1 if not existing_ids else max(existing_ids) + 1)(
            [store.store_id for store in db.query(StoreDB).all()]
        )
    db_store = StoreDB(**store_data)
    db.add(db_store)
    db.commit()
    db.refresh(db_store)
    return db_store


@router.get("/store/{store_id}", response_model=StoreResponse)
async def read_store(store_id: int, db: Session = Depends(get_db)):
    db_store = db.query(StoreDB).filter(StoreDB.store_id == store_id).first()
    if db_store is None:
        raise HTTPException(status_code=404, detail="Store not found")
    return db_store


@router.get("/store", response_model=List[StoreResponse])
async def read_stores(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    stores = db.query(StoreDB).offset(skip).limit(limit).all()
    return stores


@router.delete("/store/{store_id}", response_model=None)
async def delete_store(store_id: int, db: Session = Depends(get_db)):
    db_store = db.query(StoreDB).filter(StoreDB.store_id == store_id).first()
    if db_store is None:
        raise HTTPException(status_code=404, detail="Store not found")
    if db.query(ProductDB).filter(ProductDB.store_id == store_id).first():
        raise HTTPException(status_code=400, detail="Cannot delete store with existing products")
    db.delete(db_store)
    db.commit()


@router.post("/product", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(product_create: ProductCreate, db: Session = Depends(get_db)):
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


@router.get("/product/{product_id}", response_model=ProductResponse)
async def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(ProductDB).filter(ProductDB.product_id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@router.get("/product", response_model=List[ProductResponse])
async def read_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    products = db.query(ProductDB).offset(skip).limit(limit).all()
    return products


@router.delete("/product/{product_id}", response_model=None)
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(ProductDB).filter(ProductDB.product_id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
