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
    stmt = select(User).where(User.email == email, User.password_hash == hash_password)
    with get_db() as db:
        user = db.scalars(stmt).one_or_none()
        return user

def create_token(user_id: int, token: str):
    with get_db() as db:
        stmt = select(Token).where(Token.user_id == user_id)
        existing = db.scalars(stmt).one_or_none()
        if existing:
            existing.token = token
            db.commit()
            db.refresh(existing)
            return existing.token

        new_token = Token(user_id=user_id, token=token)
        db.add(new_token)
        db.commit()
        db.refresh(new_token)
        return new_token.token


def get_token_by_email(email: str):
    stmt = select(Token).join(User).where(User.email == email)
    with get_db() as db:
        found_token = db.scalars(stmt).one_or_none()
        return found_token

def get_user_by_token(token: str):
    stmt = select(User).join(Token).where(Token.token == token)
    with get_db() as db:
        found_user = db.scalars(stmt).one_or_none()
        return found_user


def login(email: str, password: str):
    stmt = select(User).where(User.email == email, User.password_hash == password)
    with get_db() as db:
        user = db.scalars(stmt).one_or_none()
        return user

def create_note(title: str, description: str, user_id: int):
    new_note = Notes(title=title, description=description, user_id=user_id)
    with get_db() as db:
        db.add(new_note)
        db.commit()
        db.refresh(new_note)
    return new_note

def update_note(new_title: str, new_description: str, note_id: int):
    stmt = select(Notes).join(User).where(Notes.id == note_id)
    with get_db() as db:
        note = db.scalars(stmt).first()
        if not note:
            return None
        note.description = new_description
        note.title = new_title
        db.commit()
        db.refresh(note)
    return note


def delete_note(note_id: int):
    stmt = select(Notes).where(Notes.id == note_id)
    with get_db() as db:
        note = db.scalars(stmt).first()
        if note:
            db.delete(note)
            db.commit()
            return None
        return "Note found"

def get_my_notes(user_id: int):
    stmt = select(Notes).where(Notes.user_id == user_id)
    with get_db() as db:
        notes = db.scalars(stmt).all()
        if not notes:
            return []
        return notes

def get_note_by_id(note_id: int):
    stmt = select(Notes).where(Notes.id == note_id)
    with get_db() as db:
        note = db.scalars(stmt).one_or_none()
        return note

def check_permission(user_id: int, note_id: int):
    stmt = select(Notes).where(Notes.user_id == user_id, Notes.id == note_id)
    with get_db() as db:
        note = db.scalars(stmt).one_or_none()
        return note

