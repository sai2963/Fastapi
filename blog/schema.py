from typing import List
from pydantic import BaseModel

class BlogBase(BaseModel):
    title:str
    body:str
    
    
class Blog(BlogBase):
    class Config():
        orm_mode=True
        
class user(BaseModel):
    name:str
    email:str
    password:str      
    
class showuser(BaseModel):
    name:str
    email:str
    blogs:List[Blog] = []
    class Config():
        orm_mode=True
          

class ShowBlog(BaseModel):
    title:str
    body:str
    creator:showuser
    class Config():
        orm_mode=True        
        
class Login(BaseModel):
    username:str
    password:str          