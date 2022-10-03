from random import random
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
import random

app = FastAPI()

#app.mount("/svelte-front", StaticFiles(directory="../svelte-front/public", html=True), name="svelte-front")


origins = [
    "http://localhost",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://0.0.0.0:5173",
    "https://0.0.0.0:5173",
    "http://localhost:4173",
    "http://127.0.0.1:4173",
    "http://0.0.0.0:4173",
    "https://0.0.0.0:4173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/rand")
async def rand():
    return random.randint(0, 100)

@app.get("/")
async def front():
    return RedirectResponse(url="svelte-front")