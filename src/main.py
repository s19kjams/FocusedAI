from fastapi import Depends, FastAPI
from cachetools.keys import hashkey
from src.models import *
from src.crud import *
from src.schemas import *
from src.database import setup_database
from src.cache import *

app = FastAPI()

SessionLocal, database, Base, _ = setup_database()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/courses/", response_model=Course)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    new_course = add_course(db=db, course=course)
    cache_key = hashkey("courses")
    delete_cache(cache_key)
    return new_course

@app.put("/courses/{course_id}", response_model=Course)
def update_course(course_id: int, course_data: CourseCreate, db: Session = Depends(get_db)):
    updated_course = modify_course(db=db, course_id=course_id, course_data=course_data)
    cache_key = hashkey("courses")
    delete_cache(cache_key)
    return updated_course

@app.get("/courses/", response_model=list[Course])
def get_courses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cache_key = hashkey("courses")
    cached_result = get_cache(cache_key)
    if cached_result:
        return cached_result
    
    courses = retrieve_courses(db=db, skip=skip, limit=limit)

    set_cache(cache_key, courses)

    return courses

@app.get("/courses/{course_id}", response_model=Course)
def get_course(course_id: int, db: Session = Depends(get_db)):
    return retrieve_course_by_id(db=db, course_id=course_id)

@app.delete("/courses/{course_id}", status_code=204)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    deleted_course = remove_course(db=db, course_id=course_id)
    cache_key = hashkey("courses")
    delete_cache(cache_key)
    return deleted_course

@app.post("/lessons/", response_model=Lesson)
def create_lesson(lesson: LessonCreate, db: Session = Depends(get_db)):
    new_lesson = add_lesson(db=db, lesson=lesson)
    cache_key = hashkey("lessons")
    delete_cache(cache_key)
    return new_lesson

@app.get("/lessons/", response_model=list[Lesson])
def get_lessons(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cache_key = hashkey("lessons")
    cached_result = get_cache(cache_key)
    if cached_result:
        return cached_result
    
    lessons = retrieve_lessons(db=db, skip=skip, limit=limit)

    set_cache(cache_key, lessons)

    return lessons

@app.get("/courses/{course_id}/lessons/", response_model=list[Lesson])
def get_lessons_for_course(course_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return retrieve_lessons_for_course(db=db, course_id=course_id, skip=skip, limit=limit)

@app.post("/students/", response_model=Student)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    new_student = add_student(db=db, student=student)
    cache_key = hashkey("students")
    delete_cache(cache_key)
    return new_student

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
def create_teacher(teacher: TeacherCreate, db: Session = Depends(get_db)):
    new_teacher = add_teacher(db=db, teacher=teacher)
    cache_key = hashkey("teachers")
    delete_cache(cache_key)
    return new_teacher

@app.get("/teachers/", response_model=list[Teacher])
def get_teachers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cache_key = hashkey("teachers")
    cached_result = get_cache(cache_key)
    if cached_result:
        return cached_result

    teachers = retrieve_teachers(db=db, skip=skip, limit=limit)

    set_cache(cache_key, teachers)
    return teachers

@app.post("/enrollments/")
def enroll_student(enrollment: EnrollmentCreate, db: Session = Depends(get_db)):
    new_enrollment = add_enrollment(db=db, enrollment=enrollment)
    cache_key = hashkey("enrollments")
    delete_cache(cache_key)
    return new_enrollment

@app.delete("/enrollments/{student_id}/{course_id}")
def disenroll_student(student_id: int, course_id: int, db: Session = Depends(get_db)):
    removed_enrollment = remove_enrollment(db=db, student_id=student_id, course_id=course_id)
    
    cache_key = hashkey("enrollments")
    delete_cache(cache_key)
    return removed_enrollment

@app.get("/enrollments/", response_model=list[Enrollment])
def get_enrollments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cache_key = hashkey("enrollments")
    cached_result = get_cache(cache_key)
    if cached_result:
        return cached_result

    enrollments = retrieve_enrollments(db=db, skip=skip, limit=limit)

    set_cache(cache_key, enrollments)
    return enrollments

@app.get("/students/{student_id}/enrollments/", response_model=list[Enrollment])
def get_student_enrollments(student_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    enrollments = retrieve_student_enrollments(db=db, student_id=student_id, skip=skip, limit=limit)
    return enrollments
