from typing import Optional

from fastapi import FastAPI, HTTPException
from pony.orm.core import db_session, select
from pony.orm.serialization import to_dict
from pydantic.dataclasses import dataclass
from pony.orm import Database, PrimaryKey, Required

app = FastAPI()

db = Database(provider='sqlite', filename='database.db', create_db=True)

class Post(db.Entity):
    _table_ = "Posts"
    id = PrimaryKey(int, auto=True)
    header = Required(str)
    content = Required(str)

db.generate_mapping(create_tables=True)

# http://127.0.0.1:8000/api/posts
@app.get("/api/posts")
def get_posts():
    posts = None
    with db_session:
        posts = Post.select()[:10]
        print(posts[0].to_dict() for p in posts)
    return

@app.get("/api/posts/{name}")
def get_posts(name: str):
    posts = None
    with db_session:
        posts = Post.select(lambda p: p.header == "Python")[:10]
        print(posts[0].to_dict() for p in posts)
    return