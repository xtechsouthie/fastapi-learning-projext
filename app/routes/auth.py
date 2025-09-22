from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database
from ..schemas import UserLogin
from ..models import User
from ..utils import verify
from ..oauth2 import create_access_token

router = APIRouter(tags=["Authentication"])

@router.post("/login")
def login(user_input: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(User).filter(User.email == user_input.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
    
    if not verify(user_input.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
    
    access_token = create_access_token(data= {"user_id": user.id})
    #create and return a JWT token
    return {"access_token": access_token, "token_type": "bearer"}

    
