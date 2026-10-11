from fastapi import FastAPI, HTTPException, Path, Query, Body, Depends
from typing import Optional, List, Dict, Annotated
from sqlalchemy.orm import Session

from models import Base, User, Post
from database import engine, session_local
from schemas import UserCreate, User as DbUser, PostCreate, PostResponse


app = FastAPI()


Base.metadata.create_all(bind=engine)


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=DbUser)
async def create_user(user: UserCreate, db: Session = Depends(get_db)) -> DbUser:
    db_user = User(name=user.name, age=user.age)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@app.post("/posts/", response_model=PostResponse)
async def create_post(post: PostCreate, db: Session = Depends(get_db)) -> PostResponse:
    db_user = db.query(User).filter(User.id == post.author_id).first()
    if db_user is None:
        raise HTTPException(status_code=404)

    
    db_post = Post(title=post.title, body=post.body, author_id=post.author_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    return db_post


@app.get("/posts", response_model=List[PostResponse])
async def posts(db: Session = Depends(get_db)):
    return db.query(Post).all()




# @app.get("/news")
# async def news() -> List[Post]:
#     return [Post(**post) for post in posts]


# @app.get("/news/{postid}")
# async def news(postid: Annotated[int, Path(..., title="Указывается id поста", ge=1)]) -> Post:
#     for post in posts:
#         if post['id'] == postid:
#             return Post(**post)
#     raise HTTPException(status_code=404, detail='Post not found')


# @app.get("/search")
# async def search(postid: Annotated[
#     Optional[int],
#     Query(title="id для поиска поста по id", ge=1),
#     ]) -> Dict[str, Optional[Post]]:
#     if postid:
#         for post in posts:
#                 if post['id'] == postid:
#                     return {"data": Post(**post)}
#         raise HTTPException(status_code=404, detail='Post not found')
#     else:
#         return {"data": None}


# @app.post("/news/add")
# async def create(post: PostCreate) -> Post:
#     author = next((user for user in users if user['id'] == post.author_id), None)
#     if not author:
#         raise HTTPException(status_code=404, detail="User not found")
#     new_post_id = len(posts) + 1
#     new_post = {
#         'id': new_post_id,
#         'title': post.title,
#         'body': post.body,
#         'author': author,
#     }
#     posts.append(new_post)
#     return Post(**new_post)


# @app.post("/users/add")
# async def create(user_param: Annotated[
#     UserCreate,
#     Body(..., example={
#         'name': 'UserName',
#         'age': 1,
#     })
# ]) -> User:
#     new_user_id = len(users) + 1
#     new_user = {'id': new_user_id, 'name': UserCreate.name, 'age': UserCreate.int},
#     users.append(new_user)
#     return User(**new_user)