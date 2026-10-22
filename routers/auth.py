from fastapi import APIRouter
from fastapi import Depends,HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from schemes.user import UserCreate,UserLogin
from security import pwd_context
from schemes.user import UserResponse
import datetime
import jwt 
from config import MY_ALGORITHM,MY_CODE,ACCESS_MINUTES


router=APIRouter(prefix="/auth",tags=["auth"])


@router.post("/register",response_model=UserResponse)
async def register(user:UserCreate,
                   db:Session=Depends(get_db)): 
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=409,detail="Email already registered")
    hashed_password=pwd_context.hash(user.password)

    new_user=User(email=user.email,
                  name=user.name,
                  role="user",
                  password_hash=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login")
async def login(user:UserLogin,
                db:Session=Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=401,detail="Invalid credentials")

    if not pwd_context.verify(user.password,db_user.password_hash):
        raise HTTPException(status_code=401,detail="Invalid credentials")

    exp=datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(minutes=ACCESS_MINUTES)

    payload={
        "sub":str(db_user.id),
        "exp":exp
    }

    token = jwt.encode(payload,MY_CODE, algorithm=MY_ALGORITHM)
    
    return  {
        "message": "Login successful",
        "access_token": token,
        "token_type": "bearer"
    }