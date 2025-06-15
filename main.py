from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from database import database
from schemas import UserCreate, UserOut, TodoCreate, TodoOut
from auth import authenticate_user, create_access_token, get_current_user
from crud import create_user, get_todos_by_user, create_todo, update_todo, delete_todo, get_todo_by_id, get_user
from typing import List
from datetime import timedelta

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.post("/register", response_model=UserOut)
async def register(user: UserCreate):
    existing_user = await get_user(user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    created_user = await create_user(user)
    return created_user

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={"sub": user["username"]}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me", response_model=UserOut)
async def read_users_me(current_user=Depends(get_current_user)):
    return current_user

@app.get("/todos/", response_model=List[TodoOut])
async def read_todos(current_user=Depends(get_current_user)):
    todos = await get_todos_by_user(current_user.id)
    return todos


@app.post("/todos/", response_model=TodoOut)
async def create_new_todo(todo: TodoCreate, current_user=Depends(get_current_user)):
    return await create_todo(todo, current_user.id)


@app.put("/todos/{todo_id}", response_model=TodoOut)
async def update_existing_todo(todo_id: int, todo: TodoCreate, current_user=Depends(get_current_user)):
    db_todo = await get_todo_by_id(todo_id, current_user.id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return await update_todo(todo_id, todo, current_user.id)


@app.delete("/todos/{todo_id}")
async def delete_existing_todo(todo_id: int, current_user=Depends(get_current_user)):
    db_todo = await get_todo_by_id(todo_id, current_user.id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    await delete_todo(todo_id, current_user.id)
    return {"detail": "Todo deleted"}



