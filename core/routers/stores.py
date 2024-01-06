from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi import status
from core.schemas import StoreResponse, StoreCreate
from core.models import Store as StoreDB, Product as ProductDB
from env_config import SessionLocal
from core.routers.auth import get_current_user, get_user_exception

router = APIRouter(
    prefix='/store',
    tags=['store']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/create-store", response_model=StoreResponse, status_code=status.HTTP_201_CREATED)
async def create_store(store_create: StoreCreate,
                       user: dict = Depends(get_current_user),
                       db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
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


@router.get("/get-store/{store_id}", response_model=StoreResponse)
async def read_store(store_id: int,
                     user: dict = Depends(get_current_user),
                     db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    db_store = db.query(StoreDB).filter(StoreDB.store_id == store_id).first()
    if db_store is None:
        raise HTTPException(status_code=404, detail="Store not found")
    return db_store


@router.get("/get-stores", response_model=List[StoreResponse])
async def read_stores(skip: int = 0, limit: int = 10,
                      user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    stores = db.query(StoreDB).offset(skip).limit(limit).all()
    return stores


@router.delete("/delete-store/{store_id}", response_model=None)
async def delete_store(store_id: int,
                       user: dict = Depends(get_current_user),
                       db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    db_store = db.query(StoreDB).filter(StoreDB.store_id == store_id).first()
    if db_store is None:
        raise HTTPException(status_code=404, detail="Store not found")
    if db.query(ProductDB).filter(ProductDB.store_id == store_id).first():
        raise HTTPException(status_code=400, detail="Cannot delete store with existing products")
    db.delete(db_store)
    db.commit()
