from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey
from database import metadata, engine

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String, unique=True, index=True),
    Column("hashed_password", String),
)

todos = Table(
    "todos",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String, index=True),
    Column("description", String, nullable=True),
    Column("completed", Boolean, default=False),
    Column("owner_id", Integer, ForeignKey("users.id")),
)

metadata.create_all(engine)
