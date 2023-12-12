from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import relationship
from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from databases import Database
from dotenv import load_dotenv
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from cachetools import TTLCache
from cachetools.keys import hashkey
import os

load_dotenv()

postgres_user = os.getenv('POSTGRES_USER')
postgres_password = os.getenv('POSTGRES_PASSWORD')
postgres_db = os.getenv('POSTGRES_DB')
postgres_host = os.getenv('POSTGRES_HOST')
postgres_port = os.getenv('POSTGRES_PORT')

DATABASE_URL = f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"

app = FastAPI()

database = Database(DATABASE_URL)
metadata = declarative_base()

class Course(metadata):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

class Lesson(metadata):
    __tablename__ = "lessons"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    course_id = Column(Integer, ForeignKey("courses.id"))
    course = relationship("Course", back_populates="lessons")

class User(metadata):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)

Course.lessons = relationship("Lesson", back_populates="course")

engine = create_engine(DATABASE_URL)
metadata.metadata.create_all(engine)

limiter = FastAPILimiter(key_func=lambda _: "global", redis_url=None)
limiter.init_app(app)

cache = TTLCache(maxsize=1000, ttl=60)

def get_cache(key):
    return cache.get(key)

def set_cache(key, value):
    cache[key] = value

@app.post("/courses/", response_model=Course, dependencies=[Depends(RateLimiter(times=5, seconds=10))])
async def create_course(name: str):
    query = Course.insert().values(name=name)
    course_id = await database.execute(query)
    return {"id": course_id, "name": name}

@app.get("/courses/", response_model=list[Course], dependencies=[Depends(RateLimiter(times=5, seconds=10))])
async def get_courses():
    cache_key = hashkey("get_courses")
    cached_result = get_cache(cache_key)
    if cached_result:
        return cached_result

    query = Course.select()
    result = await database.fetch_all(query)

    set_cache(cache_key, result)
    return result

@app.post("/lessons/", response_model=Lesson, dependencies=[Depends(RateLimiter(times=5, seconds=10))])
async def create_lesson(title: str, course_id: int):
    query = Lesson.insert().values(title=title, course_id=course_id)
    lesson_id = await database.execute(query)
    return {"id": lesson_id, "title": title, "course_id": course_id}

@app.get("/lessons/", response_model=list[Lesson], dependencies=[Depends(RateLimiter(times=5, seconds=10))])
async def get_lessons():
    cache_key = hashkey("get_lessons")
    cached_result = get_cache(cache_key)
    if cached_result:
        return cached_result

    query = Lesson.select()
    result = await database.fetch_all(query)

    set_cache(cache_key, result)
    return result

@app.post("/users/", response_model=User, dependencies=[Depends(RateLimiter(times=5, seconds=10))])
async def create_user(username: str):
    query = User.insert().values(username=username)
    user_id = await database.execute(query)
    return {"id": user_id, "username": username}

@app.get("/users/", response_model=list[User], dependencies=[Depends(RateLimiter(times=5, seconds=10))])
async def get_users():
    cache_key = hashkey("get_users")
    cached_result = get_cache(cache_key)
    if cached_result:
        return cached_result

    query = User.select()
    result = await database.fetch_all(query)

    set_cache(cache_key, result)
    return result
