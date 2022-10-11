import os
from dotenv import load_dotenv
from passlib.context import CryptContext
import random
import json

from fastapi import FastAPI, Request, Depends, Form, status, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login import LoginManager

from pydantic import BaseModel

from database import UserModel, Todos, users_ref

""" Trying to read in secret key """
load_dotenv()
SECRET_KEY = os.environ.get('SECRET_KEY')
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

""" Login Handling """

class NotAuthenticatedException(Exception):
    pass

manager = LoginManager(
    SECRET_KEY, 
    token_url="/docs/token", 
    use_cookie=True,
    use_header=True,
    custom_exception=NotAuthenticatedException
    )
manager.cookie_name = "my_cookie"
manager.useRequest(app)

@manager.user_loader()
async def query_firestore_user(username: str):
    user = await users_ref.document(username).get()
    user = user.to_dict()
    return user

# For hashing passwords submitted by users
def get_password_hash(password):
    return pwd_context.hash(password)

# For verifying passwords when users logging in
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_current_user(user_request: Request):
    if user_request.state.user:
        user = user_request.state.user['username']
    else:
        return None
    return user

""" CORS Handling """
origins = [
    # "http://localhost",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:4173",
    "http://127.0.0.1:4173",
    "https://dylanfair.github.io"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

""" Endpoints """

@app.get("/rand")
async def rand():
    return random.randint(0, 100)

@app.get("/")
async def front():
    return "Hi!"

# This is handles the login for /docs
@app.post("/docs/token", include_in_schema=False)
async def login(
    request: Request, 
    response: Response,
):
    json_request = await request.json()
    username = json_request.get("username")
    password = json_request.get("password")
    user = await query_firestore_user(username)

    if user is None:
        return {"message": False}

    if not verify_password(password, user['password']):
        return {"message": False}

    access_token = manager.create_access_token(
        data = {"sub": username}
    )
    
    manager.set_cookie(response, access_token)
    return {"access_token": access_token, "token_type": "bearer"}

# This handles regular login for the front end
@app.post("/token", include_in_schema=False)
async def login(
    request: Request, 
    response: Response,
    #data: OAuth2PasswordRequestForm = Depends()
):
    json_request = await request.json()
    username = json_request.get("username")
    password = json_request.get("password")
    # username = data.username
    # password = data.password
    user = await query_firestore_user(username)

    if user is None:
        return {"message": False}

    if not verify_password(password, user['password']):
        return {"message": False}

    access_token = manager.create_access_token(
        data = {"sub": username}
    )
    
    # resp = True
    # response.set_cookie(access_token)
    #resp = RedirectResponse(url="/success", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
    resp = {"message": True}
    manager.set_cookie(response, access_token)
    return resp

@app.get("/{username}/todos")
async def read_todos(request: Request, username: str):
    # username2 = user['username']
    # user_todos = user['todos']

    # return user_todos
    headers = request.headers
    if headers.get("username") == username: 
        user = await query_firestore_user(username)
        user_todos = user['todos']
        return user_todos

    # user = await query_firestore_user(username)
    # user_todos = user['todos']
    # return user_todos

    return "Error!"