import os
from dotenv import load_dotenv
from passlib.context import CryptContext
import random

from fastapi import FastAPI, Request, Depends, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login import LoginManager

#from database import UserModel, Todos, users_ref

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
    "http://localhost",
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

@app.get("/success")
async def nice():
    return "Successful login"

@app.get("/fail")
async def boo():
    return "Failed login"

# Let them log in
@app.get("/login", include_in_schema=False)
def submit_login(request: Request):
    user = get_current_user(request)
    if user is None:
        return RedirectResponse(url="/success", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
    else:
        response = RedirectResponse(url="/", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
        return response

# This handles regular login for the front end
@app.post("/token", include_in_schema=False)
async def login(request: Request, data: OAuth2PasswordRequestForm = Depends()):
    username = data.username
    password = data.password
    user = await query_firestore_user(username)

    if user is None:
        login_fail = True
        return RedirectResponse(url="/fail", status_code=status.HTTP_307_TEMPORARY_REDIRECT)

    if not verify_password(password, user['password']):
        login_fail = True
        return RedirectResponse(url="/fail", status_code=status.HTTP_307_TEMPORARY_REDIRECT)

    access_token = manager.create_access_token(
        data = {"sub": username}
    )
    
    resp = RedirectResponse(url="/success", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
    manager.set_cookie(resp, access_token)
    return resp