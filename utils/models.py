import os

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Text, Unicode
from sqlalchemy.ext.declarative import declarative_base

from utils import settings

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    uid = Column(Integer, primary_key=True)
    name = Column(Unicode)
    mail = Column(Unicode)

engine = create_engine(
    settings.DATABASE_CONNECTION_URL,
    pool_recycle=3600,
    pool_size=20,
    max_overflow=100
)

Base.metadata.bind = engine

