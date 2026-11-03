from fastapi import APIRouter,Depends,HTTPException,Query
from models.user import User
from schemes.user import UserResponse,UserUpdate,UserListResponse
from dependencies import get_current_user,require_admin
from sqlalchemy.orm import Session
from database import get_db
from services.user_service import update_user_name,delete_user
from typing import Literal
from sqlalchemy import or_

users_router=APIRouter(prefix="/user",tags=["users"])


@users_router.get("/me", response_model=UserResponse)
async def getMe(current_user:User=Depends(get_current_user)):
    return current_user

@users_router.patch("/me",response_model=UserResponse)
async def updateMe(data:UserUpdate,current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    if "name" not in  data.model_fields_set:
        raise HTTPException(status_code=400,detail="Invalid data")
    if data.name is None  or not data.name.strip():
         raise HTTPException(status_code=400,detail="Invalid data")
    update_user=update_user_name(db, current_user, data.name)
    if update_user is None:
        raise HTTPException(status_code=400,detail="Invalid data")
    return update_user

@users_router.delete("/me")
async def deleteMe(user=Depends(get_current_user),db:Session=Depends(get_db)):
    delete_user(db,user)
    return {"message":"The data has been deleted."}


@users_router.get("/",response_model=UserListResponse)
async def get_all_users(admin:User=Depends(require_admin),
                        db:Session=Depends(get_db),
                        skip:int=Query(0,ge=0),
                        limit:int=Query(10,ge=1,le=100),
                        sort_order:Literal["asc","desc"]=Query("asc"),
                        search:str|None=Query(None),
                        role:Literal["admin","user"]=Query(None)):
    query = db.query(User)
    
    #Filter name and mail
    if search:
        search = search.strip()
    if search:
        query = query.filter(or_(User.name.ilike(f"%{search}%"),User.email.ilike(f"%{search}%")))
    if role:
        query=query.filter(User.role==role)  
    count=query.count()                         
    if sort_order == "asc":
        sort_column = User.created_at.asc()
    else:
        sort_column = User.created_at.desc()
    allUsers = (query.order_by(sort_column).offset(skip).limit(limit).all()) 
          
    return {"total":count,"items":allUsers}   
    
        

