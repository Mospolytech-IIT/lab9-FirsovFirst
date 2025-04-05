from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Text, ForeignKey

from fastapi import FastAPI

SQLALCHEMY_DATABASE_URL = "sqlite:///./../test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

class Base(DeclarativeBase): pass

class Users(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

class Posts(Base):
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

SessionLocal = sessionmaker(autoflush=False, bind=engine)
db = SessionLocal()

post = db.query(Posts).filter(Posts.id == 3).first()
if post:
    db.delete(post)
    db.commit()

user_id = 1

posts = db.query(Posts).filter(Posts.user_id == user_id).all()

for post in posts:
    db.delete(post)

user = db.query(Users).filter(Users.id == user_id).first()
if user:
    db.delete(user)
    db.commit()

app = FastAPI()
