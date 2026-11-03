from fastapi import FastAPI,Depends,HTTPException,Request
from fastapi.responses import JSONResponse
import sqlalchemy
import logging
from sqlalchemy import create_engine
from database import Base, engine
from models.user import User
from models.refresh_session import RefreshSession
from schemes.user import UserCreate,UserLogin,UserResponse,UserUpdate
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm,HTTPBearer,HTTPBasic,HTTPBasicCredentials,HTTPAuthorizationCredentials
from typing import Annotated
from sqlalchemy.orm import Session
from database import get_db
from passlib.context import CryptContext
import datetime
import jwt
from config import MY_ALGORITHM,MY_CODE,ACCESS_MINUTES
from dependencies import get_current_user
from security import pwd_context
from routers.auth import router as auth_router 
from routers.users import users_router

app=FastAPI()
logger=logging.getLogger(__name__)

app.include_router(auth_router)
app.include_router(users_router)

@app.exception_handler(Exception)
async def exc_handler(request:Request,exc:Exception):
    logger.exception(f"Unhandled exception on {request.url.path}")
    return JSONResponse(status_code=500,content={"detail":"Internal server error"})

#---------------------------------------#
Base.metadata.create_all(engine)
# print(Base.metadata.tables.keys())
# print("DATABASE:", engine.url)
#---------------------------------------#


security=HTTPBearer()


