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

users = db.query(Users).all()

for u in users:
    print(f"{u.id} {u.username} {u.email}")
    print("-" * 40)

posts = db.query(Posts).all()

for p in posts:
    print(f"{p.id} {p.title} {p.content}")

    user = db.query(Users).filter(Users.id == p.user_id).first()
    if user:
        print(f"{u.id} {u.username} {u.email}")
    
    print("-" * 40)

postsFromUser = db.query(Posts).filter(Posts.user_id == 1).all()

for pfu in postsFromUser:
    print(f"{p.id} {p.title} {p.content}")
    print("-" * 40)

app = FastAPI()
