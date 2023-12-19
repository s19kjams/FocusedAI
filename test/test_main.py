from fastapi.testclient import TestClient
import sys

import pytest
sys.path.append("./src")
from src.main import *
from src.crud import *
from src.models import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

client = TestClient(app)

@pytest.fixture(scope="session")
def db():
    DATABASE_URL = "sqlite:///./test.db"
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    try:
        yield TestingSessionLocal()
    finally:
        Base.metadata.drop_all(bind=engine)

def test_create_course(db):
    teacher = Teacher(name="Test Teacher Name")
    db.add(teacher)
    db.commit()
    
    course_data = CourseCreate(name="Test Course", teacher_id=teacher.id)
    response = create_course(course_data, db)
    assert response.name == course_data.name
    assert response.teacher_id == teacher.id

def test_update_course(db):
    teacher = Teacher(name="Test Teacher Name")
    db.add(teacher)
    db.commit()
    
    course_data = CourseCreate(name="Test Course", teacher_id=teacher.id)
    response = create_course(course_data, db)
    
    updated_course_data = CourseCreate(name="Updated Test Course", teacher_id=teacher.id)
    updated_response = update_course(response.id, updated_course_data, db)
    
    assert updated_response.name == updated_course_data.name
    assert updated_response.teacher_id == teacher.id

def test_get_courses(db):
    teacher = Teacher(name="Test Teacher Name")
    db.add(teacher)
    db.commit()
    
    course_data = CourseCreate(name="Test Course", teacher_id=teacher.id)
    response = create_course(course_data, db)
    
    response = client.get("/courses/")
    assert response.status_code == 200

def test_get_course_by_id(db):
    teacher = Teacher(name="Test Teacher Name")
    db.add(teacher)
    db.commit()

    course_data = CourseCreate(name="Test Course", teacher_id=teacher.id)
    new_course = create_course(course_data, db)

    response_get_course = retrieve_course_by_id(db=db, course_id=new_course.id)
    
    assert response_get_course.name == course_data.name
    assert response_get_course.teacher_id == teacher.id

def test_delete_course(db):
    teacher = Teacher(name="Test Teacher Name")
    db.add(teacher)
    db.commit()
    
    course_data = CourseCreate(name="Test Course", teacher_id=teacher.id)
    new_course = add_course(db=db, course=course_data)
    
    response = get_courses(db=db)
    before_delete_course = len(response)
    
    response = delete_course(db=db, course_id=new_course.id)
    assert response == f"Course with ID {new_course.id} has been deleted"
    
    response = get_courses(db=db)
    assert before_delete_course == len(response) + 1

def test_create_student(db):
    student_data = StudentCreate(username="Test Student")
    response = create_student(student_data, db)
    assert response.username == student_data.username

def test_get_students(db):
    student_data = StudentCreate(username="Test Student")
    response = create_student(student_data, db)
    
    response = client.get("/students/")
    assert response.status_code == 200

def test_create_teacher(db):
    teacher_data = TeacherCreate(name="Test Teacher")
    response = create_teacher(teacher_data, db)
    assert response.name == teacher_data.name

def test_get_teachers(db):
    teacher_data = TeacherCreate(name="Test Teacher")
    response = create_teacher(teacher_data, db)
    
    response = client.get("/teachers/")
    assert response.status_code == 200

def test_create_lesson(db):
    teacher = Teacher(name="Test Teacher Name")
    db.add(teacher)
    
    course = Course(name="Test Course Name")
    db.add(course)
    db.commit()
    
    lesson_data = LessonCreate(title="Test Lesson", course_id=course.id)

    response = create_lesson(lesson_data, db)
    
    assert response.title == lesson_data.title
    assert response.course_id == course.id

def test_get_lessons(db):
    teacher = Teacher(name="Test Teacher Name")
    db.add(teacher)
    
    course = Course(name="Test Course Name", teacher_id=teacher.id)
    db.add(course)
    db.commit()
    
    lesson_data = LessonCreate(title="Test Lesson", course_id=course.id)
    create_lesson(lesson_data, db)
    
    response = client.get("/lessons/")
    assert response.status_code == 200

def test_get_lessons_for_course(db):
    teacher = Teacher(name="Test Teacher Name")
    db.add(teacher)

    course = Course(name="Test Course Name", teacher_id=teacher.id)
    db.add(course)
    db.commit()

    lesson_data = LessonCreate(title="Test Lesson", course_id=course.id)
    new_lesson = create_lesson(lesson_data, db)
    lesson_data = LessonCreate(title="Test Lesson", course_id=course.id)
    new_lesson = create_lesson(lesson_data, db)
    
    response_get_lessons_for_course = retrieve_lessons_for_course(db=db, course_id=new_lesson.course_id)

    assert any(lesson.id == new_lesson.id for lesson in response_get_lessons_for_course)


def test_create_enrollment(db):
    teacher = Teacher(name="Test Teacher Name")
    db.add(teacher)
    
    student = Student(username="Test Student Username")
    db.add(student)
    
    course = Course(name="Test Course Name", teacher_id=teacher.id)
    db.add(course)
    db.commit()

    enrollment_data = EnrollmentCreate(student_id=student.id, course_id=course.id)
    response = enroll_student(enrollment_data, db)
    
    assert response.student_id == student.id
    assert response.course_id == course.id  

def test_get_enrollments(db):
    teacher = Teacher(name="Test Teacher Name")
    db.add(teacher)
    
    course = Course(name="Test Course Name", teacher_id=teacher.id)
    db.add(course)

    student = Student(username="Test Student Username")
    db.add(student)
    db.commit()
    
    enrollment = EnrollmentCreate(course_id=course.id, student_id=student.id)
    enroll_student(enrollment, db)
    
    response = client.get("/enrollments/")
    assert response.status_code == 200

def test_delete_enrollment(db):
    teacher = Teacher(name="Test Teacher Name")
    db.add(teacher)
    
    course = Course(name="Test Course Name", teacher_id=teacher.id)
    db.add(course)

    student = Student(username="Test Student Username")
    db.add(student)
    db.commit()
    
    enrollment = EnrollmentCreate(course_id=course.id, student_id=student.id)
    enroll_student(enrollment, db)
    
    response = get_student_enrollments(student_id=student.id, db=db)
    before_disenroll = len(response)
    
    disenroll_student(student.id, course.id, db)
    response = get_student_enrollments(student_id=student.id, db=db)
    
    assert len(response) == before_disenroll - 1
    
def test_get_enrollment_for_student(db):
    teacher = Teacher(name="Test Teacher Name")
    db.add(teacher)
    
    student = Student(username="Test Student Username")
    db.add(student)
    
    course = Course(name="Test Course Name", teacher_id=teacher.id)
    db.add(course)
    db.commit()

    enrollment = EnrollmentCreate(course_id=course.id, student_id=student.id)
    enroll_student(enrollment, db)

    response = get_student_enrollments(student_id=student.id, db=db)
    assert response[-1].student_id == student.id
    assert response[-1].course_id == course.id
