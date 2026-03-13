from database import get_db
from sqlalchemy import select
from models import User, Notes, Token

def create_user(email: str, role: str, password: str):
    new_user = User(email=email, password_hash=password, role=role)
    with get_db() as db:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    return new_user

def get_user_by_data(email: str, hash_password: str):
    stmt = select(User).where(email=email, hash_password=hash_password)
    with get_db() as db:
        user = db.scalars(stmt).one()
        if not user:
            return None
        return user

def create_token(user_id: int, token: str):
    new_token = Token(user_id=user_id, token=token)
    with get_db() as db:
        db.add(new_token)
        db.commit()
        db.refresh(new_token)
    return new_token.token

def get_token_by_email(email: str):
    stmt = select(Token).where(email=email)
    with get_db() as db:
        found_token = db.scalars(stmt).one()
        if not found_token:
            return None
        return found_token

def login(email: str, password: str):
    stmt = select(User).where(email=email, password_hash=password)
    with get_db() as db:
        user = db.scalars(stmt).one()
        if not user:
            return None
        return user

