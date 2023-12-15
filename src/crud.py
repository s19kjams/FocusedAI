from sqlalchemy.orm import Session
from models import (
    Course as DBCourse,
    Teacher as DBTeacher,
    Lesson as DBLesson,
    Student as DBStudent,
    Enrollment as DBEnrollment,
)

from schemas import (
    CourseCreate, StudentCreate, TeacherCreate
)


def create_course(db: Session, course: CourseCreate):
    db_course = DBCourse(**course.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

def retrieve_courses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(DBCourse).offset(skip).limit(limit).all()

def update_course(db: Session, course_id: int, course_data: CourseCreate):
    db_course = db.query(DBCourse).filter(DBCourse.id == course_id).first()
    for key, value in course_data.dict().items():
        setattr(db_course, key, value)
    db.commit()
    db.refresh(db_course)
    return db_course

def delete_course(db: Session, course_id: int):
    db_course = db.query(DBCourse).filter(DBCourse.id == course_id).first()
    db.delete(db_course)
    db.commit()


def add_student(db: Session, student: StudentCreate):
    db_student = DBStudent(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def add_teacher(db: Session, teacher: TeacherCreate):
    db_teacher = DBTeacher(**teacher.dict())
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher


def retrieve_teachers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(DBTeacher).offset(skip).limit(limit).all()

def retrieve_students(db: Session, skip: int = 0, limit: int = 100):
    return db.query(DBStudent).offset(skip).limit(limit).all()