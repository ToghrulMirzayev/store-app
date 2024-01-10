from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)


class Store(Base):
    __tablename__ = "stores"

    store_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    store_name = Column(String, index=True)
    location = Column(String)
    address = Column(String, default=None)

    products = relationship("Product", back_populates="store")

    def __str__(self):
        return f"{self.store_name}"


class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    product_name = Column(String, index=True)
    is_available = Column(Boolean, default=True)
    store_id = Column(Integer, ForeignKey("stores.store_id"))

    store = relationship("Store", back_populates="products")

    def __str__(self):
        return f"{self.product_name}"
