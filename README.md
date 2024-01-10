# store-app

This is a simple API application built with FastAPI, a modern Python web framework. The project provides a RESTful API for managing stores and their products.

## Key Features
- **User Registration:** New users can register by providing necessary information such as email, username, password etc.
- **Authentication:** Registered users can authenticate themselves using a secure authentication mechanism.
- **Role-Based Access Control:** The application implements role-based access control (RBAC), allowing users to have specific roles, such as 'admin' or 'user'. Different roles grant different levels of access and permissions.
- **Store Management:** Enables users with appropriate roles to perform actions related to store management, including addition, retrieval, updating, and deletion of store information.
- **Product Management:** Users with the necessary roles can manage product information within stores by performing actions such as addition, retrieval, updating, and deletion of products.
## Technologies Used
- Python 3
- FastAPI
- Pydantic
- SQLAlchemy
- PostgreSQL
- Alembic

## Database Structure
```
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

stores table

| Column         | Data Type |
|----------------|-----------|
| store_id       | SERIAL    |
| store_name     | VARCHAR   |
| location       | VARCHAR   |
| address        | VARCHAR   |

products table

| Column         | Data Type |
|----------------|-----------|
| product_id     | SERIAL    |
| product_name   | VARCHAR   |
| is_available   | BOOLEAN   |
| store_id       | INTEGER   |
```

## Getting started
* Clone repository to your local machine:
  * `git clone https://github.com/ToghrulMirzayev/store-app.git`
* Create virtual env:
  * `python -m venv venv`
* Activate virtual env
  * Windows:
    * `venv/Scripts/activate`
  * MacOS/Linux:
    * `source venv/bin/activate`
* Install dependencies: 
  * `pip install -r requirements.txt`
* Setup Postgres server on your machine with no table in the database as they will be created using alembic migration
* To make this code work on your local machine, create `.env` in root directory and add environment variables there as shown in below example:
  * ```
    SECRET_KEY=unique and complex string as a secret key
    DB_USER=database user
    DB_PASS=database password
    DB_HOST=database host
    DB_PORT=database port
    DB_NAME=database name
    ```
* Run alembic migration to create tables and columns with proper data types
  * `alembic upgrade head`
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
