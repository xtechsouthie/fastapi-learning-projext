from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from typing import Optional, List
from ..utils import hash
from random import randrange
import psycopg
import time

from sqlalchemy.orm import Session
from app import models
from ..schemas import Post, UserCreate, UserOut
from ..database import session, engine, get_db
#from psycopg.extras import RealDictCursor


router = APIRouter(
    prefix="/users",
    tags= ["Users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):

    #hash the user password:
    payload.password = hash(payload.password)

    new_user = models.User(**payload.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model=UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"User with the id of id: {id} does not exists.")
    return user