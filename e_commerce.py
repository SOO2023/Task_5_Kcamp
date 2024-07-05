from fastapi import Depends, APIRouter, Form, HTTPException
import schema, database, crud
from auth import get_user
from util import RandomGen, simple_id_generator
from datetime import datetime

router = APIRouter(prefix="/e_commerce", tags=["e_commerce"])

# viewing order history, placing orders, and managing account details.
order_id_gen = simple_id_generator()
random_gen = RandomGen()


@router.get("/orders/", response_model=list[schema.Order])
def get_orders(user_id: int = Depends(get_user)):
    orders = crud.get_items(database.order_db, user_id)
    return orders


@router.get("/orders/{order_id}", response_model=schema.Order)
def get_order(order_id: int, user_id: int = Depends(get_user)):
    order = crud.get_item_by_id(database.order_db, user_id, order_id)
    return order


@router.post("/orders/", response_model=schema.Order)
def place_order(
    item_name: str = Form(), quantity: int = Form(), user_id: int = Depends(get_user)
):
    id = next(order_id_gen)
    unit_price = random_gen.random_price()
    total_price = quantity * unit_price
    delivery_duration = random_gen.random_days()
    order = schema.Order(
        id=id,
        user_id=user_id,
        item_name=item_name,
        quantity=quantity,
        unit_price=unit_price,
        total_price=total_price,
        purchase_date=datetime.now(),
        delivery_duration=f"{delivery_duration} days",
    )
    database.order_db.append(order)
    return order


@router.put("/account/", response_model=schema.Account)
def update_account(
    account_name: str = Form(),
    bank: str = Form(),
    card_type: str = Form(),
    user_id: int = Depends(get_user),
):
    account_obj = schema.Account(
        account_name=account_name, bank=bank, card_type=card_type, id=user_id
    )
    for index, account in enumerate(database.account_db):
        if account.id == user_id:
            database.account_db[index] = account_obj
            return account_obj
    raise HTTPException(status_code=400, detail="Invalid user id")


@router.get("/", response_model=schema.Account)
def get_user_account(user_id: int = Depends(get_user)):
    for account in database.account_db:
        if account.id == user_id:
            return account
