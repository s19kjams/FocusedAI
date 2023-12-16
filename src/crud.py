from sqlalchemy.orm import Session
from models import (
    Course as DBCourse,
    Teacher as DBTeacher,
    Lesson as DBLesson,
    Student as DBStudent,
    Enrollment as DBEnrollment,
)

from schemas import *
from loguru import logger


logger.add("monitoring/app.log", rotation="500 MB", backtrace=True, diagnose=True)


def add_course(db: Session, course: CourseCreate):
    try:
        db_course = DBCourse(**course.dict())
        db.add(db_course)
        db.commit()
        db.refresh(db_course)
        logger.info(f"Added course: {course.name} with ID: {db_course.id}")
        return db_course
    except Exception as e:
        logger.exception(f"Error adding course: {course.name}. Error: {str(e)}")
        raise


def retrieve_courses(db: Session, skip: int = 0, limit: int = 100):
    try:
        return db.query(DBCourse).offset(skip).limit(limit).all()
    except Exception as e:
        logger.exception(f"Error retrieving courses. Error: {str(e)}")
        raise

def update_course(db: Session, course_id: int, course_data: CourseCreate):
    try:
        db_course = db.query(DBCourse).filter(DBCourse.id == course_id).first()
        for key, value in course_data.dict().items():
            setattr(db_course, key, value)
        db.commit()
        db.refresh(db_course)

        logger.info(f"Updated course with ID: {course_id}")
        
        return db_course
    except Exception as e:
        logger.exception(f"Error updating course with ID: {course_id}. Error: {str(e)}")
        raise

def delete_course(db: Session, course_id: int):
    try:
        db_course = db.query(DBCourse).filter(DBCourse.id == course_id).first()
        db.delete(db_course)
        db.commit()

        
        logger.info(f"Deleted course with ID: {course_id}")
    except Exception as e:
        logger.exception(f"Error deleting course with ID: {course_id}. Error: {str(e)}")
        raise


def add_student(db: Session, student: StudentCreate):
    try:
        db_student = DBStudent(**student.dict())
        db.add(db_student)
        db.commit()
        db.refresh(db_student)
        
        logger.info(f"Added student: {student.name} with ID: {db_student.id}")
        
        return db_student
    except Exception as e:
        logger.exception(f"Error adding student: {student.name}. Error: {str(e)}")
        raise

def retrieve_students(db: Session, skip: int = 0, limit: int = 100):
    try:
        return db.query(DBStudent).offset(skip).limit(limit).all()
    except Exception as e:
        logger.exception(f"Error retrieving students. Error: {str(e)}")
        raise

def add_teacher(db: Session, teacher: TeacherCreate):
    try:
        db_teacher = DBTeacher(**teacher.dict())
        db.add(db_teacher)
        db.commit()
        db.refresh(db_teacher)
        
        logger.info(f"Added teacher: {teacher.name} with ID: {db_teacher.id}")
        
        return db_teacher
    except Exception as e:
        logger.exception(f"Error adding teacher: {teacher.name}. Error: {str(e)}")
        raise

def retrieve_teachers(db: Session, skip: int = 0, limit: int = 100):
    try:
        return db.query(DBTeacher).offset(skip).limit(limit).all()
    except Exception as e:
        logger.exception(f"Error retrieving teachers. Error: {str(e)}")
        raise

def add_lesson(db: Session, lesson: LessonCreate):
    try:
        db_lesson = DBLesson(**lesson.dict())
        db.add(db_lesson)
        db.commit()
        db.refresh(db_lesson)
        
        logger.info(f"Added lesson: {lesson.name} with ID: {db_lesson.id}")
        
        return db_lesson
    except Exception as e:
        logger.exception(f"Error adding lesson: {lesson.name}. Error: {str(e)}")
        raise

def retrieve_lessons(db: Session, skip: int = 0, limit: int = 100):
    try:
        return db.query(DBLesson).offset(skip).limit(limit).all()
    except Exception as e:
        logger.exception(f"Error retrieving lessons. Error: {str(e)}")
        raise

def add_enrollment(db: Session, enrollment: EnrollmentCreate):
    try:
        db_enrollment = DBEnrollment(**enrollment.dict())
        db.add(db_enrollment)
        db.commit()
        db.refresh(db_enrollment)
        
        logger.info(f"Added enrollment for student {enrollment.student_id} in course {enrollment.course_id}")
        
        return db_enrollment
    except Exception as e:
        logger.exception(f"Error adding enrollment for student {enrollment.student_id} in course {enrollment.course_id}. Error: {str(e)}")
        raise

def remove_enrollment(db: Session, student_id: int, course_id: int):
    try:
        db_enrollment = db.query(DBEnrollment).filter_by(student_id=student_id, course_id=course_id).first()
        db.delete(db_enrollment)
        db.commit()
        
        logger.info(f"Removed enrollment for student ID: {student_id} in course ID: {course_id}")
        
        return {"message": "Enrollment removed successfully"}
    except Exception as e:
        logger.exception(f"Error removing enrollment for student ID: {student_id} in course ID: {course_id}. Error: {str(e)}")
        raise

def retrieve_enrollments(db: Session, skip: int = 0, limit: int = 100):
    try:
        return db.query(DBEnrollment).offset(skip).limit(limit).all()
    except Exception as e:
        logger.exception(f"Error retrieving enrollments. Error: {str(e)}")
        raise

def retrieve_student_enrollments(db: Session, student_id: int, skip: int = 0, limit: int = 100):
    try:
        return db.query(DBEnrollment).filter(DBEnrollment.student_id == student_id).offset(skip).limit(limit).all()
    except Exception as e:
        logger.exception(f"Error retrieving enrollments for student ID: {student_id}. Error: {str(e)}")
        raise
