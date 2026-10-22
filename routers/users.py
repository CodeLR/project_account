from fastapi import APIRouter,Depends,HTTPException
from models.user import User
from schemes.user import UserResponse,UserUpdate
from dependencies import get_current_user
from sqlalchemy.orm import Session
from database import get_db
from services.user_service import update_user_name,delete_user


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