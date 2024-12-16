from fastapi import APIRouter,Depends,HTTPException,status
from .. import schema,hashing,models,database
from sqlalchemy.orm import Session
router=APIRouter()

@router.post('/user' ,response_model=schema.showuser,tags=['users'])
def create_user(request:schema.user,db:Session=Depends(database.get_db)):
    
    new_user=models.User(name=request.name,email=request.email,password=hashing.Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/user',response_model=schema.showuser,tags=['users'])
def get_user(id:int,db:Session=Depends(database.get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'user with {id} not found')
    return user