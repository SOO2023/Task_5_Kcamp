from fastapi import Depends, APIRouter, Form, HTTPException
import schema, database, util, crud
from auth import get_user
from datetime import datetime

router = APIRouter(prefix="/posts", tags=["posts"])
post_id_gen = util.simple_id_generator()


@router.get("/{post_id}/", response_model=schema.Post)
def get_post_id(post_id: int, user_id: int = Depends(get_user)):
    post = crud.get_item_by_id(database.post_db, user_id, post_id)
    return post


@router.post("/", response_model=list[schema.Post])
def create_post(
    description: str = Form(),
    content: str = Form(),
    user_id: int = Depends(get_user),
):
    id = next(post_id_gen)
    post = schema.Post(
        date=datetime.now(),
        description=description,
        content=content,
        id=id,
        user_id=user_id,
    )
    database.post_db.append(post)
    user_posts = [post for post in database.post_db if post.user_id == user_id]
    return user_posts


@router.put("/{post_id}/")
def update_post(
    post_id: int,
    description: str = Form(),
    content: str = Form(),
    user_id: int = Depends(get_user),
):
    for i, post in enumerate(database.post_db):
        if post.id == post_id:
            if post.user_id == user_id:
                database.post_db[i].content = content
                database.post_db[i].description = description
                return database.post_db[i]
    raise HTTPException(status_code=400, detail="Invalid post id")


@router.delete("/{post_id}/")
def delete_post(post_id: int, user_id: int = Depends(get_user)):
    message = crud.delete_item(database.post_db, user_id, post_id)
    return message


@router.get("/", response_model=list[schema.Post])
def get_posts(user_id: int = Depends(get_user)):
    posts = crud.get_items(database.post_db, user_id)
    return posts
