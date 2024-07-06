from pydantic import BaseModel
from datetime import datetime


class ItemBase(BaseModel):
  title: str
  description: str | None = None


class ItemCreate(ItemBase):
  pass


class Item(ItemBase):
  id: int
  owner_id: int

  class Config:
    from_attributes = True


class UserBase(BaseModel):
  email: str


class UserCreate(UserBase):
  password: str


# class User(UserBase):
#   id: int
#   is_active: bool
#   items: list[Item] = []

#   class Config:
#     orm_mode = True


class User(BaseModel):
  first_name : str
  last_name : str
  email:str
  register_date: datetime
  enabled: bool

class Student(User):
  codsis: int

class Admin(User):
  ci: str