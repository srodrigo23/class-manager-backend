from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from .database import Base
from datetime import datetime

class User(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key=True, autoincrement=True)
  first_name= Column(String)
  last_name= Column(String)
  email = Column(String, unique=True, index=True)
  register_date = Column(DateTime, default=datetime.now)
  enabled = Column(Boolean, default=True)
  student = relationship("Student")
  
class Student(Base):
  __tablename__ = "students"
  id = Column(Integer, primary_key=True, autoincrement=True)
  codsis = Column(Integer)
  user_id = Column(Integer, ForeignKey("users.id"))
  detail_career = relationship("DetailStudentCareer")

class DetailStudentCareer(Base):
  __tablename__ = "details_student_career"
  id = Column(Integer, primary_key=True, autoincrement=True)
  student_id = Column(Integer, ForeignKey("students.id"))
  career_id = Column(Integer, ForeignKey("careers.id"))
  detail_course_subject = relationship("DetailCourseSubjectStudent")

class Career(Base):
  __tablename__ = "careers"
  id = Column(Integer, primary_key=True, autoincrement=True)
  codsis = Column(Integer)
  college = Column(String)
  detail_student = relationship("DetailStudentCareer")

class Course(Base):
  __tablename__ = "courses"
  id = Column(Integer, primary_key=True, autoincrement=True)
  title = Column(String)
  start_date = Column(DateTime)
  end_date = Column(DateTime)
  detail_subject = relationship("DetailCourseSubject")

class DetailCourseSubject(Base):
  __tablename__= "details_course_subject"
  id = Column(Integer, primary_key=True, autoincrement=True)
  course_id = Column(Integer, ForeignKey("courses.id"))
  subject_id = Column(Integer, ForeignKey("subjects.id"))
  detail_student_career = relationship("DetailCourseSubjectStudent")

class Subject(Base):
  __tablename__ = "subjects"
  id = Column(Integer, primary_key=True, autoincrement=True)
  codsis = Column(Integer)
  title = Column(String)
  detail_Course = relationship("DetailCourseSubject")

class DetailCourseSubjectStudent(Base):
  __tablename__ = "details_course_subject_student"
  id = Column(Integer, primary_key=True, autoincrement=True)
  detail_course_subject_id = Column(Integer, ForeignKey("details_course_subject.id"))#relationship("DetailCourseSubject")
  detail_student_career_id = Column(Integer, ForeignKey("details_student_career.id"))#relationship("DetailStudentCareer")
  detail_grade_class =relationship("Grade")

class Grade(Base):
  __tablename__ = "grades"
  id = Column(Integer, primary_key=True)
  pp = Column(Integer)
  sp = Column(Integer)
  ef = Column(Integer)
  detail_class_id = Column(Integer, ForeignKey("details_course_subject_student.id")) #relationship("User")