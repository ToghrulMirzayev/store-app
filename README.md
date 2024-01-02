# store-app

This is a simple API application built with FastAPI, a modern Python web framework. The project provides a RESTful API for managing stores and their products.

## Key Features
- Store Management: Addition, retrieval, updating, and deletion of store information.
- Product Management: Addition, retrieval, updating, and deletion of product information within stores.
## Technologies Used
- FastAPI
- SQLAlchemy
- PostgreSQL

## Database setup
```
CREATE TABLE stores (
    store_id SERIAL PRIMARY KEY,
    store_name VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL
);

CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    is_available BOOLEAN DEFAULT TRUE,
    store_id INTEGER REFERENCES stores(store_id)
);
```

## Getting started
* Create virtual env:
  * `python -m venv venv`
* Activate virtual env
  * Windows:
    * `venv/Scripts/activate`
  * MacOS/Linux:
    * `source venv/bin/activate`
* Install dependencies: 
  * `pip install -r requirements.txt`
* Launch the server:
  * `uvicorn main:app --reload`

After this, the API will be accessible at http://127.0.0.1:8000/docs, where you can use the interactive Swagger documentation to test requests.
