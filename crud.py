import schema
from fastapi import HTTPException
from util import Hasher


def create_user(db_user, db_profile, db_acct, user: schema.User, id: int):
    password = Hasher.hash_pwd(user.password)
    user_db = schema.UserDB(id=id, username=user.username, password=password)
    db_user.append(user_db)
    user_profile = schema.Profile(
        fullname=user_db.username, email="NA", address="NA", id=user_db.id
    )
    db_profile.append(user_profile)
    default_acct_details = schema.Account(
        id=user_db.id, account_name="NA", bank="NA", card_type="NA"
    )
    db_acct.append(default_acct_details)
    return {"id": user_db.id, "username": user_db.username}


def create_item(db, item: schema.Item, user_id: int, id: int):
    item = schema.ItemDB(id=id, user_id=user_id, **item.model_dump())
    db.append(item)
    all_user_items = [item for item in db if item.user_id == user_id]
    return all_user_items


def get_item_by_id(db, user_id: int, item_id: int):
    user_items = [item for item in db if item.user_id == user_id]
    for item in user_items:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=400, detail="Invalid item id")


def get_items(db, user_id: int):
    user_items = [item for item in db if item.user_id == user_id]
    return user_items


def update_item(db, user_id: int, item_id: int, update_item: schema.Item):
    for i, item in enumerate(db):
        if item.id == item_id:
            if item.user_id == user_id:
                new_item = schema.ItemDB(
                    id=item.id, user_id=user_id, **update_item.model_dump()
                )
                db[i] = new_item
                return new_item
    raise HTTPException(status_code=400, detail="Invalid item id")


def delete_item(db, user_id: int, item_id: int):
    for i, item in enumerate(db):
        if item.id == item_id:
            if item.user_id == user_id:
                del db[i]
                return {"message": "deleted successfully!"}
    raise HTTPException(status_code=400, detail="Invalid item id")
