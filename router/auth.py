from fastapi import FastAPI,APIRouter,Depends,HTTPException
from pydantic import BaseModel,Field
from typing import Annotated,Optional
from datetime import timedelta,datetime,timezone
from sqlalchemy.orm import Session
from database import Sessionlocal
from models import Todos,Users
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt

router = APIRouter()
bcrpt_context=CryptContext(schemes=['bcrypt'],deprecated='auto')
#Auth2_Bearer=OAuth2PasswordBearer(tokenUrl='token')
Auth2_Bearer = OAuth2PasswordBearer(tokenUrl='/login')

SECRET_KEY='b97aee9e16a70fbfe6228381e6e0075f1b0b0a538be64fe8d7c70f4367672577'
ALGORITHM='HS256'

class creatUsers(BaseModel):
    email:str
    username:str
    firstname:str
    lastname:str
    password:str
    role:str
    phone_number:str

class UpdateUser(BaseModel):
   
    email:Optional[str]=Field(default=None)
    username:Optional[str]=Field(default=None)
    firstname :Optional[str]=Field(default=None)
    lastname:Optional[str]=Field(default=None)
    phone_number:Optional[str]=Field(default=None)
class Password_Change(BaseModel):
   current_pass:str
   new_pass:str

def Authenticate_User(username,password,db):
      user = db.query(Users).filter(Users.username==username).first()
      if user is None:
         return False
      if bcrpt_context.verify(password,user.hash_password):
         return user
      return False
      
def create_access_token(username:str,user_id:int,role:str,expires_delta:timedelta): 
    encode={'sub':username,'id':user_id,'role':role}
    expirse=datetime.now(timezone.utc)+expires_delta
    encode.update({'exp':expirse})
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)

def get_current_user(token: Annotated[str, Depends(Auth2_Bearer)]
):
    try:
        payload = jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM] )

        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        role:str=payload.get('role')

        if username is None or user_id is None:
            raise HTTPException(status_code=404,detail="User not Found" )

        return {"username": username, "id": user_id,"role":role}

    except Exception:
        raise HTTPException( status_code=401, detail="Invalid token")

def get_db():
    db=Sessionlocal()
    try:
      yield db
    finally:
     db.close()

db_depends=Annotated[Session,Depends(get_db)]
user_depends=Annotated[dict,Depends(get_current_user)]

@router.post('/createuser')
def user_create(db:db_depends,new_user:creatUsers):
  user_model=Users(
     email=new_user.email,
     username=new_user.username,
     firstname=new_user.firstname,
     lastname=new_user.lastname,
     hash_password=bcrpt_context.hash(new_user.password),
     is_active=True,
     role=new_user.role,
     phone_number=new_user.phone_number

  )

  db.add(user_model)
  db.commit()
  return JSONResponse(status_code=202,content=" User_Create Done")

@router.post('/login')
def login_user(db:db_depends,form_data:Annotated[OAuth2PasswordRequestForm,Depends()]):
  user =  Authenticate_User(form_data.username,form_data.password,db)
  if not user:
      raise HTTPException(status_code=401,detail="Fail")
  token=create_access_token(user.username,user.id,user.role,timedelta(minutes=30))
#   return token
  return {'access_token':token,'token_type':'bearer'}

@router.put('/edituser')
def  update_users(db:db_depends,update_user:UpdateUser,user:user_depends):
   
   if user is None:
      raise HTTPException(status_code=401,detail="User Not Login")
   
   user = db.query(Users).filter(Users.id==user.get('id')).first()
  
   update_user=update_user.model_dump(exclude_unset=True)

   for key,value in update_user.items():
      setattr(user,key,value)

   db.commit()
   return JSONResponse(status_code=202,content="User Update Done")


@router.put('/PasswordChange')
def  update_Password_Change(db:db_depends,Password_Change:Password_Change,user:user_depends):
   
   if user is None:
      raise HTTPException(status_code=401,detail="User Not Login")
   
   user = db.query(Users).filter(Users.id==user.get('id')).first()
   if not bcrpt_context.verify(Password_Change.current_pass,user.hash_password):
       raise HTTPException(status_code=401,detail="Wrong Password")
   user.hash_password =bcrpt_context.hash(Password_Change.new_pass)
   db.add(user)
   db.commit()
   return JSONResponse(status_code=202,content="Password Update Done")
      