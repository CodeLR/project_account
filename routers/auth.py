from fastapi import APIRouter
from fastapi import Depends,HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from schemes.user import UserCreate,UserLogin,RefreshRequest
from security import pwd_context,create_token
from schemes.user import UserResponse
import datetime
import jwt 
from config import MY_ALGORITHM,MY_CODE,ACCESS_MINUTES
import hashlib
from models.refresh_session import RefreshSession


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

    token, access_expire = create_token(db_user.id, "access")
    refresh_token, refresh_expire = create_token(db_user.id, "refresh")

    token_hash = hashlib.sha256(refresh_token.encode()).hexdigest()

    session = RefreshSession(
        user_id=db_user.id,
        token_hash=token_hash,
        expires_at=refresh_expire
    )

    db.add(session)
    db.commit()
    
    return  {
        "message": "Login successful",
        "access_token": token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/refresh")
async def refresh_token(request:RefreshRequest,db:Session=Depends(get_db)):
    try:
        payload=jwt.decode(request.refresh_token,MY_CODE,algorithms=[MY_ALGORITHM])
        if not payload.get("sub"):
            raise HTTPException(status_code=401,detail="Invalid credentials")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401,detail="Invalid credentials")
    if payload.get("type")!="refresh":
        raise HTTPException(status_code=401,detail="Invalid credentials")
    user_id=int(payload["sub"])
    token_hash = hashlib.sha256(request.refresh_token.encode()).hexdigest()

    session = db.query(RefreshSession).filter(RefreshSession.token_hash == token_hash).first()

    if not session or session.revoked:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    if session.expires_at <= datetime.datetime.now(datetime.timezone.utc):
        raise HTTPException(status_code=401, detail="Refresh token expired")


    user=db.query(User).filter(User.id==user_id).first()
    if not user:
        raise HTTPException(status_code=401,detail="Invalid credentials")
    if session.user_id != user_id:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    token, access_expire = create_token(user_id, "access")
    refresh_token, refresh_expire = create_token(user_id, "refresh")
    session.revoked = True

    new_token_hash = hashlib.sha256(refresh_token.encode()).hexdigest()

    new_session = RefreshSession(
        user_id=user_id,
        token_hash=new_token_hash,
        expires_at=refresh_expire
    )

    db.add(new_session)
    db.commit()


    return {
        "message": "Token refreshed successfully",
        "access_token": token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
    
@router.post("/logout")
async def logout(request: RefreshRequest, db: Session = Depends(get_db)):
    token_hash = hashlib.sha256(request.refresh_token.encode()).hexdigest()
    session = db.query(RefreshSession).filter(RefreshSession.token_hash == token_hash).first()
    
    if not session or session.revoked:
        raise HTTPException(status_code=401, detail="Invalid refresh token") 
    session.revoked=True
    db.commit() 
    return {"message": "Logged out successfully"}       