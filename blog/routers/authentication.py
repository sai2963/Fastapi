from fastapi import APIRouter,Depends,HTTPException,status
from .. import schema ,database,models,token
from sqlalchemy.orm import Session
from ..hashing import Hash
from datetime import datetime, timedelta, timezone
router=APIRouter(tags=['Login'])

@router.post('/login')
def Login(request:schema.Login ,db: Session=Depends(database.get_db)):
    user=db.query(models.User).filter(models.User.email==request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail='Invalid Credentials')
    if not Hash.verify(user.password,request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail='Incorrect Password')
        
    
    access_token = token.create_access_token(data={"sub": user.email})
    
    return {"access_token":access_token, "token_type":"bearer"}