from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Store(Base):
    __tablename__ = "stores"

    store_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    store_name = Column(String, index=True)
    location = Column(String)

    products = relationship("Product", back_populates="store")


class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    product_name = Column(String, index=True)
    is_available = Column(Boolean, default=True)
    store_id = Column(Integer, ForeignKey("stores.store_id"))

    store = relationship("Store", back_populates="products")
