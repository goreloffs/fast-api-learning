from fastapi import FastAPI, HTTPException, Path, Query, Body
from typing import Optional, List, Dict, Annotated
from pydantic import BaseModel, Field

app = FastAPI()


class User(BaseModel):
    id: int
    name: str
    age: int


class Post(BaseModel):
    id: int
    title: str
    body: str
    author: User


class PostCreate(BaseModel):
    title: str
    body: str
    author_id: int


class UserCreate(BaseModel):
    name: Annotated[
        str, Field(..., title='имя пользователя', min_length=2, max_length=20)
    ]
    age: Annotated[
        int, Field(..., title='возраст пользователя', ge=0, le=120)
    ]


users = [
    {'id': 1, 'name': 'Timofey', 'age': 22},
    {'id': 2, 'name': 'Ivan', 'age': 22},
    {'id': 3, 'name': 'Anton', 'age': 22},
]


posts = [
        {'id': 1, 'title': 'name1', 'body': 'tex1', "author": users[0]},
        {'id': 2, 'title': 'name2', 'body': 'tex2', "author": users[1]},
        {'id': 3, 'title': 'name3', 'body': 'tex3', "author": users[2]},
]


@app.get("/news")
async def news() -> List[Post]:
    return [Post(**post) for post in posts]


@app.get("/news/{postid}")
async def news(postid: Annotated[int, Path(..., title="Указывается id поста", ge=1)]) -> Post:
    for post in posts:
        if post['id'] == postid:
            return Post(**post)
    raise HTTPException(status_code=404, detail='Post not found')


@app.get("/search")
async def search(postid: Annotated[
    Optional[int],
    Query(title="id для поиска поста по id", ge=1),
    ]) -> Dict[str, Optional[Post]]:
    if postid:
        for post in posts:
                if post['id'] == postid:
                    return {"data": Post(**post)}
        raise HTTPException(status_code=404, detail='Post not found')
    else:
        return {"data": None}


@app.post("/news/add")
async def create(post: PostCreate) -> Post:
    author = next((user for user in users if user['id'] == post.author_id), None)
    if not author:
        raise HTTPException(status_code=404, detail="User not found")
    new_post_id = len(posts) + 1
    new_post = {
        'id': new_post_id,
        'title': post.title,
        'body': post.body,
        'author': author,
    }
    posts.append(new_post)
    return Post(**new_post)


@app.post("/users/add")
async def create(user_param: Annotated[
    UserCreate,
    Body(..., example={
        'name': 'UserName',
        'age': 1,
    })
]) -> User:
    new_user_id = len(users) + 1
    new_user = {'id': new_user_id, 'name': UserCreate.name, 'age': UserCreate.int},
    users.append(new_user)
    return User(**new_user)