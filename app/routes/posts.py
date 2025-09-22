from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from typing import Optional, List
from ..utils import hash
from random import randrange
import psycopg
import time

from sqlalchemy.orm import Session
from .. import models, oauth2
from ..schemas import Post, UserCreate, UserOut
from ..database import session, engine, get_db

#from psycopg.extras import RealDictCursor


router = APIRouter(
    prefix="/posts",  #this is the prefix for the link address to avoid typing /posts again and again in @get method.
    tags= ["Posts"]   #this tags the posts routes together in the api /docs
    #tags is a list, you can put multiple tags for a router
    )

@router.get("/", response_model=List[Post])
async def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_post(payLoad: Post, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (payLoad.title, payLoad.content, payLoad.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**payLoad.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=Post)
def return_post(id: int, response: Response, db: Session = Depends(get_db)):
    test_post = db.query(models.Post).filter(models.Post.id == id).first()
    if not test_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id of {id} not found")
    return test_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, response: Response, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # deleted_post = cursor.fetchone()
    deleted_post = db.query(models.Post).filter(models.Post.id == id).first()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id of {id} not found")
    db.delete(deleted_post)
    db.commit()
    print(deleted_post)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=Post)
def update_posts(id: int, updated_post: Post, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id of {id} not found")
    post_query.update(updated_post.model_dump())
    db.commit()
    return post_query.first()