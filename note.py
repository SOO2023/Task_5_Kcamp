from fastapi import Depends, APIRouter, Form
import schema, database, util, crud
from auth import get_user

router = APIRouter(prefix="/notes", tags=["notes"])
note_id_gen = util.simple_id_generator()


@router.get("/{note_id}/", response_model=schema.ItemDB)
def get_note_id(note_id: int, user_id: int = Depends(get_user)):
    note = crud.get_item_by_id(database.note_db, user_id, note_id)
    return note


@router.post("/", response_model=list[schema.ItemDB])
def create_note(
    description: str = Form(),
    content: str = Form(),
    user_id: int = Depends(get_user),
):
    id = next(note_id_gen)
    note = schema.Item(description=description, content=content)
    user_notes = crud.create_item(database.note_db, note, user_id, id)
    return user_notes


@router.put("/{note_id}/")
def update_note(
    note_id: int,
    description: str = Form(),
    content: str = Form(),
    user_id: int = Depends(get_user),
):
    update_note = schema.Item(description=description, content=content)
    new_note = crud.update_item(database.note_db, user_id, note_id, update_note)
    return new_note


@router.delete("/{note_id}/")
def delete_note(note_id: int, user_id: int = Depends(get_user)):
    message = crud.delete_item(database.note_db, user_id, note_id)
    return message


@router.get("/", response_model=list[schema.ItemDB])
def get_notes(user_id: int = Depends(get_user)):
    notes = crud.get_items(database.note_db, user_id)
    return notes
