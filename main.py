
from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()


@app.get("/blog")
def Home(limit,published:bool):
    if(published):
        return {"blog":f"{limit} published blog List"}
    else:
        return {"blog":f"{limit}  blog List"}

@app.get("/blog/unpublished")
def unpublished():
    return {"blog":"Unpublished Blogs"}

@app.get("/blog/{id}")
def blog(id : int):
    return {"blog":id}

@app.get("/blog/{id}/comments")
def comments(id : int):
    return {"blog":{1,2}}
class Blog(BaseModel):
    title:str
    body:str
    published:bool=True
@app.post('/blog')
def create_blog(blog:Blog):
    return {"data":f"Blog is created with title as {blog.title}"}
