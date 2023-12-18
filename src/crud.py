from functools import wraps
from sqlalchemy.orm import Session
from src.models import (
    Course as DBCourse,
    Teacher as DBTeacher,
    Lesson as DBLesson,
    Student as DBStudent,
    Enrollment as DBEnrollment,
)

from src.schemas import *
from loguru import logger

logger.add("monitoring/app.log", rotation="500 MB", backtrace=True, diagnose=True)

def handle_exceptions(message):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"{message}: {str(e)}")
                raise

        return wrapper

    return decorator

@handle_exceptions("Error adding course")
def add_course(db: Session, course: CourseCreate):
    db_course = DBCourse(**course.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    logger.info(f"Added course: {course.name} with ID: {db_course.id}")
    return db_course

@handle_exceptions("Error retreiving courses")
def retrieve_courses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(DBCourse).offset(skip).limit(limit).all()

@handle_exceptions("Error updating course")
def modify_course(db: Session, course_id: int, course_data: CourseCreate):
    db_course = db.query(DBCourse).filter(DBCourse.id == course_id).first()
    for key, value in course_data.dict().items():
        setattr(db_course, key, value)
    db.commit()
    db.refresh(db_course)

    logger.info(f"Updated course with ID: {course_id}")
    
    return db_course

@handle_exceptions("Error deleting course")
def remove_course(db: Session, course_id: int):
    db_course = db.query(DBCourse).filter(DBCourse.id == course_id).first()
    db.delete(db_course)
    db.commit()
    logger.info(f"Deleted course with ID: {course_id}")
    return f"Course with ID {course_id} has been deleted"

@handle_exceptions("Error adding student")
def add_student(db: Session, student: StudentCreate):
    db_student = DBStudent(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    
    logger.info(f"Added student: {student.username} with ID: {db_student.id}")
    
    return db_student

@handle_exceptions("Error retrieving students")
def retrieve_students(db: Session, skip: int = 0, limit: int = 100):
    return db.query(DBStudent).offset(skip).limit(limit).all()

@handle_exceptions("Error adding teacher")
def add_teacher(db: Session, teacher: TeacherCreate):
    db_teacher = DBTeacher(**teacher.dict())
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    
    logger.info(f"Added teacher: {teacher.name} with ID: {db_teacher.id}")
    
    return db_teacher

@handle_exceptions("Error retrieving teachers")
def retrieve_teachers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(DBTeacher).offset(skip).limit(limit).all()

@handle_exceptions("Error adding lesson")
def add_lesson(db: Session, lesson: LessonCreate):
    db_lesson = DBLesson(**lesson.dict())
    db.add(db_lesson)
    db.commit()
    db.refresh(db_lesson)
    
    logger.info(f"Added lesson: {lesson.title} with ID: {db_lesson.id}")
    
    return db_lesson

@handle_exceptions("Error retrieving lessons")
def retrieve_lessons(db: Session, skip: int = 0, limit: int = 100):
    return db.query(DBLesson).offset(skip).limit(limit).all()

@handle_exceptions("Error adding enrollment")
def add_enrollment(db: Session, enrollment: EnrollmentCreate):
    db_enrollment = DBEnrollment(**enrollment.dict())
    db.add(db_enrollment)
    db.commit()
    db.refresh(db_enrollment)
    
    logger.info(f"Added enrollment for student {enrollment.student_id} in course {enrollment.course_id}")
    
    return db_enrollment

@handle_exceptions("Error removing enrollment")
def remove_enrollment(db: Session, student_id: int, course_id: int):
    db_enrollment = db.query(DBEnrollment).filter_by(student_id=student_id, course_id=course_id).first()
    db.delete(db_enrollment)
    db.commit()
    
    logger.info(f"Removed enrollment for student ID: {student_id} in course ID: {course_id}")
    
    return {"message": "Enrollment removed successfully"}

@handle_exceptions("Error retrieving enrollments")
def retrieve_enrollments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(DBEnrollment).offset(skip).limit(limit).all()

@handle_exceptions("Error retrieving student enrollments")
def retrieve_student_enrollments(db: Session, student_id: int, skip: int = 0, limit: int = 100):
    return db.query(DBEnrollment).filter(DBEnrollment.student_id == student_id).offset(skip).limit(limit).all()
