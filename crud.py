from models import users, todos
from schemas import UserCreate, TodoCreate
from database import database
from auth import get_password_hash

# User operations
async def create_user(user: UserCreate):
    hashed_password = get_password_hash(user.password)
    query = users.insert().values(username=user.username, hashed_password=hashed_password)
    user_id = await database.execute(query)
    return {**user.dict(), "id": user_id}


# Todo operations
async def get_todos_by_user(user_id: int):
    query = todos.select().where(todos.c.owner_id == user_id)
    return await database.fetch_all(query)


async def get_todo_by_id(todo_id: int, user_id: int):
    query = todos.select().where(todos.c.id == todo_id).where(todos.c.owner_id == user_id)
    return await database.fetch_one(query)


async def create_todo(todo: TodoCreate, user_id: int):
    query = todos.insert().values(
        title=todo.title,
        description=todo.description,
        completed=todo.completed,
        owner_id=user_id,
    )
    todo_id = await database.execute(query)
    return {**todo.dict(), "id": todo_id, "owner_id": user_id}


async def update_todo(todo_id: int, todo: TodoCreate, user_id: int):
    query = todos.update().where(todos.c.id == todo_id).where(todos.c.owner_id == user_id).values(
        title=todo.title,
        description=todo.description,
        completed=todo.completed,
    )
    await database.execute(query)
    return await get_todo_by_id(todo_id, user_id)


async def delete_todo(todo_id: int, user_id: int):
    query = todos.delete().where(todos.c.id == todo_id).where(todos.c.owner_id == user_id)
    return await database.execute(query)

async def get_user(username: str):
    query = users.select().where(users.c.username == username)
    user = await database.fetch_one(query)
    return user