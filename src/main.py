from fastapi import Depends, FastAPI
from cachetools import TTLCache
from cachetools.keys import hashkey
from database import *
from models import *
from crud import *
from schemas import *
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
    return add_course(db=db, course=course)

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
def create_lesson(lesson: LessonCreate, db: Session = Depends(get_db)):
    return add_lesson(db=db, lesson=lesson)


@app.get("/lessons/", response_model=list[Lesson])
def get_lessons(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cache_key = hashkey("lessons")
    cached_result = get_cache(cache_key)
    if cached_result:
        return cached_result
    
    lessons = retrieve_lessons(db=db, skip=skip, limit=limit)

    set_cache(cache_key, lessons)

    return lessons


@app.post("/students/", response_model=Student)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    return add_student(db=db, student=student)


@app.get("/students/", response_model=list[Student])
def get_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cache_key = hashkey("students")
    cached_result = get_cache(cache_key)
    if cached_result:
        return cached_result

    students = retrieve_students(db=db, skip=skip, limit=limit)

    set_cache(cache_key, students)
    return students


@app.post("/teachers/", response_model=Teacher)
def create_student(teacher: TeacherCreate, db: Session = Depends(get_db)):
    return add_teacher(db=db, teacher=teacher)


@app.get("/teachers/", response_model=list[Teacher])
def get_teachers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cache_key = hashkey("teachers")
    cached_result = get_cache(cache_key)
    if cached_result:
        return cached_result

    teachers = retrieve_teachers(db=db, skip=skip, limit=limit)

    set_cache(cache_key, teachers)
    return teachers

@app.post("/enroll/{student_id}/{course_id}/")
def enroll_student(student_id: int, course_id: int):
    query = Enrollment.insert().values(student_id=student_id, course_id=course_id)
    database.execute(query)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)