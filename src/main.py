from fastapi import Depends, FastAPI
from cachetools import TTLCache
from cachetools.keys import hashkey
from database import *
from models import *
from crud import *
from schemas import *
import redis
import uvicorn

app = FastAPI()

cache = TTLCache(maxsize=1000, ttl=60)

def get_cache(key):
    return cache.get(key)

def set_cache(key, value):
    cache[key] = value

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/courses/", response_model=Course)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    return create_course(db=db, course=course)

@app.get("/courses/", response_model=list[Course])
def get_courses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cache_key = hashkey("courses")
    cached_result = get_cache(cache_key)
    if cached_result:
        return cached_result
    
    courses = retrieve_courses(db=db, skip=skip, limit=limit)

    set_cache(cache_key, courses)

    return courses


@app.post("/lessons/", response_model=Lesson)
def create_lesson(title: str, course_id: int):
    query = Lesson.insert().values(title=title, course_id=course_id)
    lesson_id = database.execute(query)
    return {"id": lesson_id, "title": title, "course_id": course_id}


@app.get("/lessons/", response_model=list[Lesson])
def get_lessons():
    cache_key = hashkey("get_lessons")
    cached_result = get_cache(cache_key)
    if cached_result:
        return cached_result

    query = Lesson.select()
    result = database.fetch_all(query)

    set_cache(cache_key, result)
    return result


@app.post("/students/", response_model=Student)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    return add_student(db=db, student=student)


@app.get("/students/", response_model=list[Student])
def get_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cache_key = hashkey("get_students")
    cached_result = get_cache(cache_key)
    if cached_result:
        return cached_result

    students = retrieve_students(db=db, skip=skip, limit=limit)

    set_cache(cache_key, students)
    return students


@app.post("/teachers/", response_model=Teacher)
def create_teacher(name: str):
    query = Teacher.insert().values(name=name)
    teacher_id = database.execute(query)
    return {"id": teacher_id, "name": name}

@app.get("/teachers/", response_model=list[Teacher])
def get_teachers():
    cache_key = hashkey("get_teachers")
    cached_result = get_cache(cache_key)
    if cached_result:
        return cached_result

    query = Teacher.select()
    result = database.fetch_all(query)

    set_cache(cache_key, result)
    return result

@app.post("/enroll/{student_id}/{course_id}/")
def enroll_student(student_id: int, course_id: int):
    query = Enrollment.insert().values(student_id=student_id, course_id=course_id)
    database.execute(query)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)