from sqlalchemy.orm import Session

from . import models

from . import schemas


def get_user(db: Session, user_id: int):
  return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email_by_codsis(db: Session, email: str, codsis: str):
  from sqlalchemy import or_
  return db.query(models.User, models.Student)\
    .join(models.User, models.Student.user_id == models.User.id).\
      filter(
        or_(
          models.User.email == email, 
          models.Student.codsis==codsis
        )
      ).all()

def get_users(db: Session, skip: int = 0, limit: int = 100):
  return db.query(models.User).offset(skip).limit(limit).all()

def create_student(db:Session, student: schemas.Student):
  
  db_user = models.User(
    first_name = student.first_name,
    last_name = student.last_name,
    email=student.email,
    register_date=student.register_date,
    enabled=False,
  )
  db.add(db_user)
  db.commit()
  db.refresh(db_user)
  
  db_student = models.Student(
    codsis = student.codsis,
    user_id = db_user.id
  )

  db.add(db_student)
  db.commit()
  db.refresh(db_student)
  return db_user

def create_user(db: Session, user: schemas.User):
  fake_hashed_password = user.password + "notreallyhashed"
  db_user = models.User(
    email=user.email, 
    hashed_password=fake_hashed_password
  )
  db.add(db_user)
  db.commit()
  db.refresh(db_user)
  return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
  return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
  db_item = models.Item(
    **item.dict(), 
    owner_id=user_id
  )
  db.add(db_item)
  db.commit()
  db.refresh(db_item)
  return db_item