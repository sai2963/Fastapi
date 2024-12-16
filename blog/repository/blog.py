
from fastapi import HTTPException,status
from .. import models

def get_all(db):
    blogs=db.query(models.Blog).all()
    return blogs

def add_blog(db,request):
    new_blog = models.Blog(title=request.title, body=request.body ,user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog

def get_byId(id,response,db):
    blog=db.query(models.Blog).filter(models.Blog.id ==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The blog {id} is not found")
       
    return blog

def delete(id,db):
    db.query(models.Blog).filter(models.Blog.id== id).delete(synchronize_session=False)
    db.commit()
    return 'done'

def update(id,request,db):
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