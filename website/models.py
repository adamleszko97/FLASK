from enum import unique
from flask import session
from . import db
from flask_login import UserMixin
from . import login
from sqlalchemy import Column, String, Integer, UniqueConstraint
from . import engine
from sqlalchemy.orm import sessionmaker

class users(db, UserMixin):

    __tablename__ = 'users'
    __table_args__ = (UniqueConstraint('email'),)
    id = Column(Integer, primary_key=True)
    email = Column(String(50))
    password = Column(String)

class employees(db):

    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    phone_number = Column(String)
    department = Column(String)

#db.metadata.create_all(engine)

Session = sessionmaker(engine)
session = Session()    
@login.user_loader
def load_user(id):

    return session.query(users).get(int(id))

session.close()

