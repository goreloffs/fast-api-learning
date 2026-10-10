from fastapi import FastAPI, HTTPException
from typing import Optional

app = FastAPI()


@app.get("/")
async def home() -> str:
    startpage = {"data": "hello world!"}
    return startpage["data"]


@app.get("/contacts")
async def contacts() -> int:
    return 34


posts = [
        {'id': 1, 'title': 'name1', 'body': 'tex1'},
        {'id': 2, 'title': 'name2', 'body': 'tex2'},
        {'id': 3, 'title': 'name3', 'body': 'tex3'},
]


@app.get("/news")
async def news():
    return posts


@app.get("/news/{postid}")
async def news(postid: int) -> dict:
    for post in posts:
        if post['id'] == postid:
            return post
    raise HTTPException(status_code=404, detail='Post not found')


@app.get("/search")
async def search(postid: Optional[int] = None) -> dict:
    if postid:
        for post in posts:
                if post['id'] == postid:
                    return post
        raise HTTPException(status_code=404, detail='Post not found')
    else:
        return {"data": "no post"}