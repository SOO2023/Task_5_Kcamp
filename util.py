from passlib.context import CryptContext
import random

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher:
    @staticmethod
    def hash_pwd(password: str):
        return pwd_context.hash(password)

    @staticmethod
    def verify_pwd(password: str, hash_password: str):
        return pwd_context.verify(password, hash_password)


def simple_id_generator():
    i = 0
    while True:
        i += 1
        yield i


class RandomGen:
    @staticmethod
    def random_price():
        return random.choice([12, 18, 22, 101, 17, 99, 29])

    @staticmethod
    def random_days():
        return random.choice([1, 2, 3, 4, 5])
