import uvicorn
from fastapi import FastAPI, HTTPException, status, Response, Cookie
from quires import (create_user, login, create_token, get_user_by_data, get_token_by_email)
from service import hash_password, generate_token


app = FastAPI()

@app.post("/register")
def register_user(email: str, password: str, role: str):
    password_h = hash_password(password=password)
    user = create_user(email=email, password=str(password_h), role=role)
    return user

@app.post("/login")
def login_user(email: str, password: str, response: Response):
    password_h = hash_password(password=password)
    user_found = get_user_by_data(email=email, hash_password=password_h)
    if not user_found:
        raise HTTPException(detail="Incorrect password or username", status_code=status.HTTP_400_BAD_REQUEST)
    token = generate_token()
    save_token = create_token(user_id=user_found.id, token=token)
    response.set_cookie(key="token_for_login", value=token)
    return HTTPException(detail="Success", status_code=status.HTTP_200_OK)




if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)