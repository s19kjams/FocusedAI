from typing import ForwardRef, List, Optional
from pydantic import BaseModel

class CourseBase(BaseModel):
    name: str
    teacher_id: int

class CourseCreate(CourseBase):
    pass

class Course(CourseBase):
    id: int

    class Config:
        orm_mode = True

class TeacherBase(BaseModel):
    name: str

class TeacherCreate(TeacherBase):
    pass

class Teacher(TeacherBase):
    id: int
    courses: List[Course] = []

    class Config:
        orm_mode = True

class LessonBase(BaseModel):
    title: str

class LessonCreate(LessonBase):
    pass

class Lesson(LessonBase):
    id: int
    course_id: int

    class Config:
        orm_mode = True

class StudentBase(BaseModel):
    username: str

class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    id: int
    enrollments: List["Enrollment"] = [] 

    class Config:
        orm_mode = True

class EnrollmentBase(BaseModel):
    student_id: int
    course_id: int

class EnrollmentCreate(EnrollmentBase):
    pass

class Enrollment(EnrollmentBase):
    id: int
    student: ForwardRef("Student")
    course: ForwardRef("Course")

    class Config:
        orm_mode = True

Student.update_forward_refs()
Enrollment.update_forward_refs()