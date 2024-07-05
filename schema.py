from pydantic import BaseModel
from datetime import datetime


# --------------------------------------------
# task 1 schema
# --------------------------------------------


class User(BaseModel):
    username: str
    password: str


class UserDB(User):
    id: int


class Item(BaseModel):
    description: str
    content: str


class ItemDB(Item):
    id: int
    user_id: int


class Profile(BaseModel):
    id: int
    fullname: str
    email: str
    address: str


class Post(ItemDB):
    date: datetime


class Account(BaseModel):
    id: int
    account_name: str
    bank: str
    card_type: str


class Order(BaseModel):
    id: int
    user_id: int
    item_name: str
    quantity: int
    unit_price: int
    total_price: int
    purchase_date: datetime
    delivery_duration: str
