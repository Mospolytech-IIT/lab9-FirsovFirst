from database import *
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, Body
from fastapi.responses import JSONResponse, FileResponse

# создаем таблицы
Base.metadata.create_all(bind=engine)

app = FastAPI()

# определяем зависимость
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users")
def main():
    return FileResponse("./templates/users.html")

@app.get("/api/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(Users).all()

@app.get("/api/users/{id}")
def get_user(id, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.id == id).first()
    if user==None:  
        return JSONResponse(status_code=404, content={ "message": "Пользователь не найден"})
    return user

@app.post("/api/users")
def create_user(data  = Body(), db: Session = Depends(get_db)):
    user = Users(username=data["username"], email=data["email"], password=data["password"])
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@app.put("/api/users")
def edit_user(data  = Body(), db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.id == data["id"]).first()

    if user == None: 
        return JSONResponse(status_code=404, content={ "message": "Пользователь не найден"})

    user.username = data["username"]
    user.email = data["email"]
    user.password = data["password"]
    db.commit()
    db.refresh(user)
    return user

@app.delete("/api/users/{id}")
def delete_user(id, db: Session = Depends(get_db)):
    posts = db.query(Posts).filter(Posts.user_id == id).all()

    for post in posts:
        db.delete(post)

    user = db.query(Users).filter(Users.id == id).first()

    if user == None:
        return JSONResponse( status_code=404, content={ "message": "Пользователь не найден"})

    db.delete(user)
    db.commit()
    return user

@app.get("/posts")
def main():
    return FileResponse("./templates/posts.html")

@app.get("/api/posts")
def get_posts(db: Session = Depends(get_db)):
    return db.query(Posts).all()

@app.get("/api/posts/{id}")
def get_post(id, db: Session = Depends(get_db)):
    post = db.query(Posts).filter(Posts.id == id).first()
    if post==None:  
        return JSONResponse(status_code=404, content={ "message": "Пост не найден"})
    return post

@app.post("/api/posts")
def create_post(data  = Body(), db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.id == data["user_id"]).first()

    if user == None:
        return JSONResponse( status_code=404, content={ "message": "Пользователь не найден"})

    post = Posts(title=data["title"], content=data["content"], user_id=data["user_id"])
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@app.put("/api/posts")
def edit_post(data  = Body(), db: Session = Depends(get_db)):
    post = db.query(Posts).filter(Posts.id == data["id"]).first()

    if post == None:
        return JSONResponse(status_code=404, content={ "message": "Пост не найден"})

    user = db.query(Users).filter(Users.id == data["user_id"]).first()

    if user == None:
        return JSONResponse( status_code=404, content={ "message": "Пользователь не найден"})
    
    post.title = data["title"]
    post.content = data["content"]
    post.user_id = data["user_id"]
    db.commit()
    db.refresh(post)
    return post

@app.delete("/api/posts/{id}")
def delete_post(id, db: Session = Depends(get_db)):
    post = db.query(Posts).filter(Posts.id == id).first()

    if post == None:
        return JSONResponse( status_code=404, content={ "message": "Пост не найден"})

    db.delete(post)
    db.commit()
    return post
