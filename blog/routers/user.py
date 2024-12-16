from fastapi import APIRouter,Depends,HTTPException,status
from .. import schema,hashing,models,database
from sqlalchemy.orm import Session
from ..repository import user
router=APIRouter(prefix='/user',tags=['users']
)

@router.post('/' ,response_model=schema.showuser)
def create_user(request:schema.user,db:Session=Depends(database.get_db)):
    
    return user.create_user(request,db)

@router.get('/',response_model=schema.showuser)
def get_user(id:int,db:Session=Depends(database.get_db)):
    return user.get_user(id,db)