from fastapi import FastAPI,Depends,status,Response,HTTPException
from . import schema,models
from .database import engine,SessionLocal
from sqlalchemy.orm import Session
from typing import List
from .hashing import Hash
app =FastAPI()
models.Base.metadata.create_all(engine)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()    
@app.get('/')
def Home():
    return "Blog:Blog Data"

@app.post('/blog',status_code=status.HTTP_201_CREATED,tags=['blogs'])
def create(request:schema.Blog,db:Session=Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body ,user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog

@app.get('/blog' ,response_model=List[schema.ShowBlog],tags=['blogs'])
def all(db:Session=Depends(get_db)):
    blogs=db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}',status_code=status.HTTP_200_OK,response_model=schema.ShowBlog,tags=['blogs'])
def show(id,respone:Response,db:Session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id ==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The blog {id} is not found")
        
    return blog
@app.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT,tags=['blogs'])
def destroy(id,db:Session=Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id== id).delete(synchronize_session=False)
    db.commit()
    return 'done'

@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED,tags=['blogs'])
def update(id: int, request: schema.Blog, db: Session = Depends(get_db)):
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



@app.post('/user' ,response_model=schema.showuser,tags=['users'])
def create_user(request:schema.user,db:Session=Depends(get_db)):
    
    new_user=models.User(name=request.name,email=request.email,password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/user',response_model=schema.showuser,tags=['users'])
def get_user(id:int,db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'user with {id} not found')
    return user
        