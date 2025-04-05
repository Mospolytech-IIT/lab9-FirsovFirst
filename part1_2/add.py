from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
from sqlalchemy import  Column, Integer, String, Text, ForeignKey

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

users = [
    Users(username='user1', email='user1@example.com', password='password1'),
    Users(username='user2', email='user2@example.com', password='password2'),
    Users(username='user3', email='user3@example.com', password='password3'),
]
db.add_all(users)
db.commit()

posts = [
    Posts(title='Post 1', content='Content of post 1', user_id=1),
    Posts(title='Post 2', content='Content of post 2', user_id=1),
    Posts(title='Post 3', content='Content of post 3', user_id=2),
]
db.add_all(posts)
db.commit()

app = FastAPI()
