from passlib.context import CryptContext
import jwt
from datetime import datetime,timedelta,timezone
from config import MY_ALGORITHM,MY_CODE,ACCESS_MINUTES,REFRESH_TOKEN_DAYS
import uuid


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_token(user_id:int,token_type:str):
    if token_type=="access":
        expires_delta=timedelta(minutes=ACCESS_MINUTES)
    elif token_type=="refresh":    
        expires_delta=timedelta(days=REFRESH_TOKEN_DAYS)
    else:
        raise ValueError("Invalid token type")


    
    expire=datetime.now(timezone.utc)+expires_delta
    payload={
        "sub":str(user_id),
        "type":token_type,
        "exp":expire,
        "jti":str(uuid.uuid4())
    }
    token = jwt.encode(payload,MY_CODE,algorithm=MY_ALGORITHM)
    return token,expire