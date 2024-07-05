from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, APIRouter, HTTPException
import jwt
from database import user_db
from util import Hasher


SECRET_KEY = "omobabaolowo"
ALGORITHM = "HS256"

router = APIRouter(prefix="/auth", tags=["login"])

# task 1 oauth scheme
oauth_scheme = OAuth2PasswordBearer("/auth/login/")


def get_user(token: str = Depends(oauth_scheme)):
    payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
    user_id = payload.get("user")
    return user_id


@router.post("/login/")
def login1(form: OAuth2PasswordRequestForm = Depends()):
    username = form.username
    password = form.password

    db_usernames = [user.username for user in user_db]
    if username not in db_usernames:
        raise HTTPException(status_code=401, detail="username or password not correct")
    for i, user in enumerate(user_db):
        if user.username == username:
            user_index = i
            user_hashed_pwd = user.password
    if not Hasher.verify_pwd(password, user_hashed_pwd):
        raise HTTPException(status_code=401, detail="username or password not correct")
    user_class = user_db[user_index]
    payload = {"user": user_class.id}
    encoded_token = jwt.encode(payload, SECRET_KEY, ALGORITHM)

    return {"access_token": encoded_token, "token_type": "bearer"}
