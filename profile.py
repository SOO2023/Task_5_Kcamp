from fastapi import Depends, APIRouter, Form, HTTPException
import schema, database
from auth import get_user

router = APIRouter(prefix="/profile", tags=["profile"])


@router.put("/", response_model=schema.Profile)
def update_profile(
    fullname: str = Form(),
    email: str = Form(),
    address: str = Form(),
    user_id: int = Depends(get_user),
):
    profile_obj = schema.Profile(
        fullname=fullname, email=email, address=address, id=user_id
    )
    for index, profile in enumerate(database.profile_db):
        if profile.id == user_id:
            database.profile_db[index] = profile_obj
            return profile_obj
    raise HTTPException(status_code=400, detail="Invalid user id")


@router.get("/", response_model=schema.Profile)
def get_user_profile(user_id: int = Depends(get_user)):
    for profile in database.profile_db:
        if profile.id == user_id:
            return profile
