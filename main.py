from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy.orm import Session
import models
from  pydantic import BaseModel,Field
from models import Todos,Users
from typing import Annotated
from database import engine,Sessionlocal
from fastapi.responses import JSONResponse
from typing import Optional
app=FastAPI()
from router import auth,admin
from router.auth import get_current_user

app.include_router(auth.router)
app.include_router(admin.router)
models.Base.metadata.create_all(bind=engine)

class Todo(BaseModel):
    id :int
    title :str
    description:str=Field(max_length=100)
    priority :int=Field(gt=0,lt=6)
    completed:bool

class TodoUpdate(BaseModel):
    # id :Optional[int]
    title :Optional[str]=Field(default=None)
    description:Optional[str]=Field(default=None,max_length=100)
    priority :Optional[int]=Field(default=None,gt=0,lt=6)
    completed:Optional[bool]=Field(default=None)

def get_db():
    db=Sessionlocal()
    try:
      yield db
    finally:
     db.close()

db_depends=Annotated[Session,Depends(get_db)]
user_depends=Annotated[dict,Depends(get_current_user)]

@app.get('/')
def  read_todos(db:db_depends,user:user_depends):
    if user is None:
        raise HTTPException(status_code=401,detail="User Not Login")
    return db.query(Todos).filter(Todos.owner_id==user.get('id')).all()

@app.get('/todo/{todo_id}')
def  read_todos_id(db:db_depends,todo_id:int,user:user_depends):
   if user is None:
        raise HTTPException(status_code=401,detail="User Not Login")
   todo_id = db.query(Todos).filter(Todos.owner_id==user.get('id')).filter(Todos.id==todo_id).first()
   if todo_id is not None:
      return todo_id
   else:
      raise HTTPException(status_code=404,detail="Not Found")

@app.post('/create')
def todo_create(db:db_depends,new_todo:Todo,user:user_depends):
  if user is None:
     raise HTTPException(status_code=401,detail="User Not Login")
  todo_model=Todos(**new_todo.model_dump(),owner_id=user.get('id'))
  db.add(todo_model)
  db.commit()
  return JSONResponse(status_code=202,content="Create Done")

@app.put('/edit/{todo_id}')
def  update_todos(db:db_depends,todo_id:int,update_todo:TodoUpdate,user:user_depends):
   
   if user is None:
      raise HTTPException(status_code=401,detail="User Not Login")
   todo = db.query(Todos).filter(Todos.owner_id==user.get('id')).filter(Todos.id==todo_id).first()

   if todo is None:
    raise HTTPException(status_code=404,detail="Not Found")

   update_data=update_todo.model_dump(exclude_unset=True)

   for key,value in update_data.items():
      setattr(todo,key,value)

   db.commit()
   return JSONResponse(status_code=202,content="Update Done")
      

@app.delete('/delete/{todo_id}')
def  delete_todos(db:db_depends,todo_id:int,user:user_depends):
   if user is None:
      raise HTTPException(status_code=401,detail="User Not Login")
   todo = db.query(Todos).filter(Todos.owner_id==user.get('id')).filter(Todos.id==todo_id).first()

   if todo is None:
    raise HTTPException(status_code=404,detail="Not Found")
   db.query(Todos).filter(Todos.owner_id==user.get('id')).filter(Todos.id==todo_id).first().delete()
   db.commit()
   return JSONResponse(status_code=202,content="Deleted Done")
      
      
@app.get('/user')
def  users_View_Profile(db:db_depends,user:user_depends):
    if user is None:
        raise HTTPException(status_code=401,detail="User Not Login")
    return db.query(Users).filter(Users.id==user.get('id')).first()
