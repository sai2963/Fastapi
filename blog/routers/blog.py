from fastapi import APIRouter,Depends,status,Response,HTTPException
from .. import schema ,models ,database
from typing import List
from sqlalchemy.orm import Session
from ..repository import blog
router=APIRouter(prefix='/blog',tags=['blogs'])
@router.get('/' ,response_model=List[schema.ShowBlog])
def all(db:Session=Depends(database.get_db)):
    return blog.get_all(db)

@router.post('/',status_code=status.HTTP_201_CREATED)
def create(request:schema.Blog,db:Session=Depends(database.get_db)):
    
    return blog.add_blog(db,request)

@router.get('/{id}',status_code=status.HTTP_200_OK,response_model=schema.ShowBlog)
def show(id:int,respone:Response,db:Session=Depends(database.get_db)):
    return blog.get_byId(id,respone,db)
    

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def destroy(id=int,db:Session=Depends(database.get_db)):
    return blog.delete(id,db)

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schema.Blog, db: Session = Depends(database.get_db)):
    return blog.update(id,request,db)

