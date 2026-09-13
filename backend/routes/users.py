from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from databases import get_db
import models
from hashing import hash  
from JWTtoken import create_access_token
router = APIRouter(prefix="/users", tags=['Users API'])

class UserCreate(BaseModel):
    username: str
    email: str 
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True 


@router.post('/register', response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    

    existing_user = db.query(models.DBuser).filter(models.DBuser.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")


    hashed_pwd = hash.bcrypt(user.password)


    new_user = models.DBuser(
        username=user.username,
        email=user.email,
        password=hashed_pwd
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)


    return new_user


class UserLogin(BaseModel):
    email: str
    password: str

@router.post('/login')
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.DBuser).filter(models.DBuser.email == user_credentials.email).first()
    
    if not user:
        raise HTTPException(status_code=403, detail="Invalid Credentials (Email not found)")
        
    is_password_correct = hash.verify(user.password, user_credentials.password)
    
    if not is_password_correct:
        raise HTTPException(status_code=403, detail="Invalid Credentials (Wrong Password)")
        
    access_token = create_access_token(data={"user_email": user.email})
    
    return {
        "access_token": access_token, 
        "token_type": "bearer"
    }

