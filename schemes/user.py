from pydantic import BaseModel
from pydantic import EmailStr

class UserCreate(BaseModel):
    email:EmailStr
    password:str
    name:str


class UserLogin(BaseModel):
    email:EmailStr
    password:str

class UserResponse(BaseModel):
    id:int
    name:str
    email:EmailStr
    role:str    



class UserUpdate(BaseModel):
    name:str|None=None