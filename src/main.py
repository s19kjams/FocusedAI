from fastapi import Depends, FastAPI
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
    __tablename__ = "course"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    teacher_id = Column(Integer, ForeignKey("teacher.id"))
    teacher = relationship("Teacher", back_populates="courses")
    lessons = relationship("Lesson", back_populates="course")
    students = relationship("Student", secondary="enrollment", back_populates="enrolled_courses")

class Teacher(metadata):
    __tablename__ = "teacher"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    courses = relationship("Course", back_populates="teacher")

class Lesson(metadata):
    __tablename__ = "lesson"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    course_id = Column(Integer, ForeignKey("course.id"))
    course = relationship("Course", back_populates="lessons")

class Student(metadata):
    __tablename__ = "student"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    enrolled_courses = relationship("Course", secondary="enrollment", back_populates="students")
    

class Enrollment(metadata):
    __tablename__ = "enrollment"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student.id"))
    course_id = Column(Integer, ForeignKey("course.id"))
    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")


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
def create_course(name: str, teacher_id: int):
    query = Course.insert().values(name=name, teacher_id=teacher_id)
    course_id = database.execute(query)
    return {"id": course_id, "name": name, "teacher_id": teacher_id}

@app.get("/courses/", response_model=list[Course], dependencies=[Depends(RateLimiter(times=5, seconds=10))])
def get_courses():
    cache_key = hashkey("get_courses")
    cached_result = get_cache(cache_key)
    if cached_result:
        return cached_result

    query = Course.select()
    result = database.fetch_all(query)

    set_cache(cache_key, result)
    return result


@app.post("/lessons/", response_model=Lesson, dependencies=[Depends(RateLimiter(times=5, seconds=10))])
def create_lesson(title: str, course_id: int):
    query = Lesson.insert().values(title=title, course_id=course_id)
    lesson_id = database.execute(query)
    return {"id": lesson_id, "title": title, "course_id": course_id}


@app.get("/lessons/", response_model=list[Lesson], dependencies=[Depends(RateLimiter(times=5, seconds=10))])
def get_lessons():
    cache_key = hashkey("get_lessons")
    cached_result = get_cache(cache_key)
    if cached_result:
        return cached_result

    query = Lesson.select()
    result = database.fetch_all(query)

    set_cache(cache_key, result)
    return result


@app.post("/students/", response_model=Student, dependencies=[Depends(RateLimiter(times=5, seconds=10))])
def create_student(username: str):
    query = Student.insert().values(username=username)
    student_id = database.execute(query)
    return {"id": student_id, "username": username}


@app.get("/students/", response_model=list[Student], dependencies=[Depends(RateLimiter(times=5, seconds=10))])
def get_students():
    cache_key = hashkey("get_students")
    cached_result = get_cache(cache_key)
    if cached_result:
        return cached_result

    query = Student.select()
    result = database.fetch_all(query)

    set_cache(cache_key, result)
    return result


@app.post("/teachers/", response_model=Teacher, dependencies=[Depends(RateLimiter(times=5, seconds=10))])
def create_teacher(name: str):
    query = Teacher.insert().values(name=name)
    teacher_id = database.execute(query)
    return {"id": teacher_id, "name": name}

@app.get("/teachers/", response_model=list[Teacher], dependencies=[Depends(RateLimiter(times=5, seconds=10))])
def get_teachers():
    cache_key = hashkey("get_teachers")
    cached_result = get_cache(cache_key)
    if cached_result:
        return cached_result

    query = Teacher.select()
    result = database.fetch_all(query)

    set_cache(cache_key, result)
    return result

@app.post("/enroll/{student_id}/{course_id}/", dependencies=[Depends(RateLimiter(times=5, seconds=10))])
def enroll_student(student_id: int, course_id: int):
    query = Enrollment.insert().values(student_id=student_id, course_id=course_id)
    database.execute(query)
