from fastapi import FastAPI, HTTPException
from typing import Optional, List, Dict
from pydantic import BaseModel

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
    post_obj = []
    for post in posts:
        post_obj.append(Post(id=post['id'], title=post['title'], body=post['body'])) 
    return [Post(**post) for post in posts]


@app.get("/news/{postid}")
async def news(postid: int) -> Post:
    for post in posts:
        if post['id'] == postid:
            return Post(**post)
    raise HTTPException(status_code=404, detail='Post not found')


@app.get("/search")
async def search(postid: Optional[int] = None) -> Dict[str, Optional[Post]]:
    if postid:
        for post in posts:
                if post['id'] == postid:
                    return {"data": Post(**post)}
        raise HTTPException(status_code=404, detail='Post not found')
    else:
        return {"data": None}