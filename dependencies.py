import jwt
from config import MY_ALGORITHM,MY_CODE
from fastapi import HTTPException,Depends
from sqlalchemy.orm import Session
from fastapi.security import HTTPAuthorizationCredentials,HTTPBearer
from models.user import User
from database import get_db


security=HTTPBearer()


def get_current_user(credential:HTTPAuthorizationCredentials=Depends(security),db:Session=Depends(get_db)):
    try:
        payload=jwt.decode(credential.credentials,MY_CODE,algorithms=[MY_ALGORITHM])
        if payload["type"]!="access":
            raise HTTPException(status_code=401,detail="Invalid credentials")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401,detail="Invalid credentials")

    user_id=payload.get("sub")

    if not user_id:
        raise HTTPException(status_code=401,detail="Invalid credentials"
    )
    
    try:
        user_id = int(user_id)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    except TypeError:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    
    if user_id <= 0:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )
    
    db_user=db.query(User).filter(User.id == user_id).first()
        
    
    if not db_user:
        raise HTTPException(status_code=401,detail="Invalid credentials")
    return db_user



def require_admin(user:User=Depends(get_current_user)):
    if user.role=="admin":
        return user
    raise HTTPException(status_code=403,detail="Admin access required")
        