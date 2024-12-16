from fastapi import APIRouter,Depends,status,Response,HTTPException
from .. import schema ,models ,database
from typing import List
from sqlalchemy.orm import Session
router=APIRouter()
@router.get('/blog' ,response_model=List[schema.ShowBlog],tags=['blogs'])
def all(db:Session=Depends(database.get_db)):
    blogs=db.query(models.Blog).all()
    return blogs

@router.post('/blog',status_code=status.HTTP_201_CREATED,tags=['blogs'])
def create(request:schema.Blog,db:Session=Depends(database.get_db)):
    new_blog = models.Blog(title=request.title, body=request.body ,user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog

@router.get('/blog/{id}',status_code=status.HTTP_200_OK,response_model=schema.ShowBlog,tags=['blogs'])
def show(id,respone:Response,db:Session=Depends(database.get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id ==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The blog {id} is not found")
        
    return blog

@router.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT,tags=['blogs'])
def destroy(id,db:Session=Depends(database.get_db)):
    db.query(models.Blog).filter(models.Blog.id== id).delete(synchronize_session=False)
    db.commit()
    return 'done'

@router.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED,tags=['blogs'])
def update(id: int, request: schema.Blog, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'Blog with id {id} not found')
    
   
    blog.update({
        'title': request.title, 
        'body': request.body
    })
    
    db.commit()
    return blog.first()