from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, ForeignKey, Text

from fastapi import FastAPI

# Определяем строку подключения к базе данных
SQLALCHEMY_DATABASE_URL = "sqlite:///./../test.db"

# Инициализируем движок SQLAlchemy
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Создаем базовый класс для определения моделей
class Base(DeclarativeBase): pass

# Определяем модель Users
class Users(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

# Определяем модель Posts
class Posts(Base):
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

# Генерируем таблицы в базе данных
Base.metadata.create_all(bind=engine)

# Создаем приложение FastAPI, которое пока не выполняет никаких действий
app = FastAPI()
