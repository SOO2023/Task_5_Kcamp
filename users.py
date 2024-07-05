from fastapi import APIRouter, Form
import schema, crud, database, util


router = APIRouter(prefix="/users", tags=["users"])
user_id_gen = util.simple_id_generator()


@router.post("/")
def create_user(username: str = Form(), password: str = Form()):
    id = next(user_id_gen)
    user = schema.User(username=username, password=password)

    user_dict = crud.create_user(
        database.user_db, database.profile_db, database.account_db, user, id
    )
    return user_dict


@router.get("/")
def users():
    return database.user_db
