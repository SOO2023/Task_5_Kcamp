from fastapi import Depends, APIRouter, Form
import schema, crud, database, util
from auth import get_user

router = APIRouter(prefix="/todos", tags=["todos"])
todo_id_gen = util.simple_id_generator()


@router.get("/{todo_id}/", response_model=schema.ItemDB)
def get_todo_id(todo_id: int, user_id: int = Depends(get_user)):
    todo = crud.get_item_by_id(database.to_list_db, user_id, todo_id)
    return todo


@router.post("/", response_model=list[schema.ItemDB])
def create_todos(
    description: str = Form(),
    content: str = Form(),
    user_id: int = Depends(get_user),
):
    id = next(todo_id_gen)
    todo = schema.Item(description=description, content=content)
    user_todos = crud.create_item(database.to_list_db, todo, user_id, id)
    return user_todos


@router.put("/{todo_id}/")
def update_todo(
    todo_id: int,
    description: str = Form(),
    content: str = Form(),
    user_id: int = Depends(get_user),
):
    update_todo = schema.Item(description=description, content=content)
    new_todo = crud.update_item(database.to_list_db, user_id, todo_id, update_todo)
    return new_todo


@router.delete("/{todo_id}/")
def delete_todo(todo_id: int, user_id: int = Depends(get_user)):
    message = crud.delete_item(database.to_list_db, user_id, todo_id)
    return message


@router.get("/", response_model=list[schema.ItemDB])
def get_todos(user_id: int = Depends(get_user)):
    todos = crud.get_items(database.to_list_db, user_id)
    return todos
