
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from typing import Optional, List
from .utils import hash
from random import randrange
import psycopg
import time

from sqlalchemy.orm import Session
from . import models
from .schemas import Post, UserCreate, UserOut
from .database import session, engine, get_db
from .routes import posts, users, auth
#from psycopg.extras import RealDictCursor

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
    
# while True:
#     try:
#         conn = psycopg.connect(host='localhost', dbname='fastapi', user='postgres', password='#99pancakes') 
#         #, cursor_factory=RealDictCursor
#         cursor = conn.cursor()
#         print("database was successfully connected")
#         break
#     except Exception as error:
#         print("Error occurred while connecting to the database")
#         print("Errror: ", error)
#         time.sleep(2)
        

@app.get("/")
async def root():
    return {"message": "welcome to my crib motherfucing nigg"}

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)