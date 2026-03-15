
from pydantic import BaseModel


class RegisterRequest(BaseModel):
    email: str
    password: str
    role: str = "user"


class LoginRequest(BaseModel):
    email: str
    password: str

class UserOut(BaseModel):
    email: str

class NoteRequest(BaseModel):
    title: str
    description: str = None

class NotesList(BaseModel):
    title: str
    description: str
    user: UserOut = None