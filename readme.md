# Todo List API with User Authentication

A simple RESTful API built with FastAPI that allows users to register, log in, and manage their own todo items. Includes secure password hashing and input validation using Pydantic.

---

## Features

- User registration and login with hashed passwords  
- JWT-based authentication for protected routes  
- CRUD operations for todos linked to authenticated users  
- Input validation on user and todo data  
- Async database operations using SQLite and Databases package  
- Auto-generated interactive API docs with Swagger UI (`/docs`)

---

## Tech Stack

- Python 3.10+  
- FastAPI  
- SQLite (file-based database)  
- Databases (async DB connection)  
- Pydantic (data validation)  
- Passlib (password hashing)  
- PyJWT (JWT token handling)

---

## Setup & Run

1. Clone the repo and enter directory:

   ```bash
   git clone https://github.com/yourusername/todo-api.git
   cd todo-api

## Create and activate Python environment

python3 -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

## Install dependencies

pip install -r requirements.txt

## Run the app

uvicorn main:app --reload

