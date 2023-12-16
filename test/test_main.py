from fastapi.testclient import TestClient
import sys

import pytest
sys.path.append("./src")
from main import *
from crud import *
from models import *

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

def test_get_courses():
    response = client.get("/courses/")
    assert response.status_code == 200

def test_create_student(db):
    student_data = StudentCreate(username="Test Student")
    response = create_student(student_data, db)
    assert response.username == student_data.username

def test_get_students():
    response = client.get("/students/")

    assert response.status_code == 200

def test_create_teacher(db):
    teacher_data = TeacherCreate(name="Test Teacher")
    response = create_teacher(teacher_data, db)
    assert response.name == teacher_data.name

def test_get_teachers():
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

def test_get_lessons():
    response = client.get("/lessons/")
    assert response.status_code == 200

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

def test_get_enrollment():
    response = client.get("/enrollments/")
    assert response.status_code == 200

def test_delete_enrollment(db):
    teacher = Teacher(name="Test Teacher Name")
    db.add(teacher)
    
    course = Course(name="Test Course Name", teacher_id=teacher.id)
    db.add(course)

    student = Student(username="Test Student Username")
    db.add(student)
    
    enrollment = Enrollment(course_id=course.id, student_id=student.id)
    db.add(enrollment)
    db.commit()
    
    response = disenroll_student(student.id, course.id, db)
    assert response.student_id == student.id
    
def test_get_enrollment_for_student(db):
    teacher = Teacher(name="Test Teacher Name")
    db.add(teacher)
    
    student = Student(username="Test Student Username")
    db.add(student)
    
    course = Course(name="Test Course Name", teacher_id=teacher.id)
    db.add(course)

    enrollment = Enrollment(course_id=course.id, student_id=student.id)
    db.add(enrollment)
    db.commit()

    response = get_enrollments(db=db)
    response = get_student_enrollments(student_id=student.id, db=db)
    assert response[-1].student_id == student.id
    assert response[-1].course_id == course.id
