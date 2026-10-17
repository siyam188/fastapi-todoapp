from fastapi import FastAPI,APIRouter,Depends,HTTPException
from pydantic import BaseModel
from typing import Annotated
from datetime import timedelta,datetime,timezone
from sqlalchemy.orm import Session
from database import Sessionlocal
from models import Todos,Users
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt
from router.auth import get_current_user
router = APIRouter()

def get_db():
    db=Sessionlocal()
    try:
      yield db
    finally:
     db.close()

db_depends=Annotated[Session,Depends(get_db)]
user_depends=Annotated[dict,Depends(get_current_user)]


@router.get('/admin/todo')
def  read_all_admin(db:db_depends,user:user_depends):
    if user is None or user !='admin':
        raise HTTPException(status_code=401,detail="User Not Login")
    return db.query(Todos).all()


@router.delete('/admin/delete/{todo_id}')
def  admin_delete_todos(db:db_depends,todo_id:int,user:user_depends):
   if user is None or user !='admin':
      raise HTTPException(status_code=401,detail="User Not Login")
   todo = db.query(Todos).filter(Todos.id==todo_id).first()

   if todo is None :
    raise HTTPException(status_code=404,detail="Not Found")
   db.query(Todos).filter(Todos.id==todo_id).first().delete()
   db.commit()
   return JSONResponse(status_code=202,content="Deleted Done")
      
      