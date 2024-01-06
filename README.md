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

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE,
    username VARCHAR(255) UNIQUE,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    hashed_password VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    role VARCHAR(255)
);
```

## Tables should look like below
```
stores table

| Column         | Data Type |
|----------------|-----------|
| store_id       | SERIAL    |
| store_name     | VARCHAR   |
| location       | VARCHAR   |

products table

| Column         | Data Type |
|----------------|-----------|
| product_id     | SERIAL    |
| product_name   | VARCHAR   |
| is_available   | BOOLEAN   |
| store_id       | INTEGER   |

users table

| Column         | Data Type |
|----------------|-----------|
| id             | SERIAL    |
| email          | VARCHAR   |
| username       | VARCHAR   |
| first_name     | VARCHAR   |
| last_name      | VARCHAR   |
| hashed_password| VARCHAR   |
| is_active      | BOOLEAN   |
| role           | VARCHAR   |
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
* To make this code work in your local machine, create `.env` in root directory and add environment variables there as shown in below example:
  * ```
    DATABASE_URL="your postgresql connection string"
    SECRET_KEY="your secret key"
    ```
* Launch the server:
  * Basic Launch
    * `uvicorn app:app`
    * Swagger will be accessible at http://127.0.0.1:8000/docs
  * Auto-Reload Enabled 
    * `uvicorn app:app --reload`
    * Swagger will be accessible at http://127.0.0.1:8000/docs
  * Specify Port with Auto-Reload
    * `uvicorn app:app --port 8086 --reload`
    * Swagger will be accessible at http://127.0.0.1:8086/docs
