import uvicorn
from fastapi import FastAPI, HTTPException, status, Response, Request, Depends
from pydantic import BaseModel
from quires import (create_user, create_token, get_user_by_data, get_user_by_token,
    create_note, update_note, delete_note, get_my_notes, check_permission, get_note_by_id)
from service import hash_password, generate_token
from schemas import RegisterRequest, LoginRequest, NoteRequest, NotesList
app = FastAPI()




def user_to_dict(user):
    return {"id": user.id, "email": user.email, "role": user.role}

def get_current_user(request: Request):
    token = request.cookies.get("token_for_login")
    if not token:
        raise HTTPException(detail="Not authenticated", status_code=status.HTTP_401_UNAUTHORIZED)
    user = get_user_by_token(token)
    if not user:
        raise HTTPException(detail="Invalid token", status_code=status.HTTP_400_BAD_REQUEST)
    return user

@app.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(body: RegisterRequest):
    hashed = hash_password(password=body.password)
    try:
        user = create_user(email=body.email, password=hashed, role=body.role)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    return user_to_dict(user)


@app.post("/login")
def login_user(body: LoginRequest, response: Response):
    hashed = hash_password(password=body.password)
    user_found = get_user_by_data(email=body.email, hash_password=hashed)
    if not user_found:
        raise HTTPException(detail="Incorrect password or username", status_code=status.HTTP_400_BAD_REQUEST)

    token = generate_token()
    create_token(user_id=user_found.id, token=token)
    response.set_cookie(key="token_for_login", value=token, httponly=True)

    return {"message": "Success", "token": token, "user": user_to_dict(user_found)}

@app.post("/add-note")
def add_notes(body: NoteRequest, current_user = Depends(get_current_user)):
    note = create_note(title=body.title, description=body.description, user_id=current_user.id)
    return {"message": "success", "notes": note}


@app.get("/check-token")
def check_token(token: str):
    user = get_user_by_token(token)
    if not user:
        raise HTTPException(detail="Invalid token", status_code=status.HTTP_401_UNAUTHORIZED)
    return {"message": "success", "user": user_to_dict(user)}


@app.get("/get-my-notes")
def get_notes(current_user = Depends(get_current_user)):
    notes = get_my_notes(user_id=current_user.id)
    return {"message": "success", "notes": notes}


@app.get("/note/{note_id}")
def get_note(note_id: int, current_user = Depends(get_current_user)):
    note = get_note_by_id(note_id=note_id)
    if not note:
        raise HTTPException(detail="Note not found", status_code=status.HTTP_404_NOT_FOUND)
    if note.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(detail="No permission", status_code=status.HTTP_403_FORBIDDEN)
    return {"message": "success", "note": note}


@app.put("/update-note/{note_id}")
def patch_note(note_id: int, body: NoteRequest, current_user = Depends(get_current_user)):
    note = get_note_by_id(note_id=note_id)
    if not note:
        raise HTTPException(detail="Note not found", status_code=status.HTTP_404_NOT_FOUND)
    if note.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(detail="No permission", status_code=status.HTTP_403_FORBIDDEN)
    updated = update_note(new_title=body.title, new_description=body.description, note_id=note_id)
    if not updated:
        raise HTTPException(detail="Update failed", status_code=status.HTTP_400_BAD_REQUEST)
    return {"message": "success", "note": updated}


@app.delete("/delete/{note_id}")
def delete_notes(note_id: int, current_user = Depends(get_current_user)):
    user_id = current_user.id
    note_id = note_id
    if not check_permission(user_id=user_id, note_id=note_id) and current_user.role != "admin":
        return HTTPException(detail="No permission", status_code=status.HTTP_403_FORBIDDEN)
    found = delete_note(note_id=note_id)
    if not found:
        return HTTPException(detail="No found", status_code=status.HTTP_404_NOT_FOUND)
    return {"message": "success"}

    


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)