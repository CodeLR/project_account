from sqlalchemy.orm import Session
from models.user import User

import logging

logger=logging.getLogger(__name__)



def update_user_name(db:Session,user:User,name:str):
    if not name.strip():
        return None
    user.name=name.strip()
    try:
        db.commit()
    except Exception: 
        db.rollback()
        logger.exception("Failed to save user changes")
        raise
    db.refresh(user)
    return user 


def delete_user(db:Session,user:User):
    db.delete(user)
    try:
        db.commit()
        return True
    except Exception: 
        db.rollback()
        logger.exception("Failed to delete user")
        raise
    
 
    

