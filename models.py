__author__ = 'nnduc_000'

from sqlalchemy import *
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base

import settings


def db_connect():
    return create_engine(URL(**settings.DATABASE))

DeclarativeBase = declarative_base()


def create_table(engine):
    DeclarativeBase.metadata.create_all(engine)


class JobData(DeclarativeBase):
    __tablename__ = "job_finland"
    id = Column(Integer, primary_key=True)
    title = Column('title', String)
    link = Column('link', String)
    location = Column('location', String)
    description = Column('description', String)
    source = Column('source', String)  # where we take data from

    # if the jobs is created by company this will be 1 otherwise, it will be 0
    sponsor = Column('sponsor', Integer, nullable=True)
    company_name = Column('company_name', String, nullable=True)
    expire_day = Column('expire_day', DateTime, nullable=True)


class JobData_Estonia(DeclarativeBase):
    __tablename__ = "job_estonia"
    id = Column(Integer, primary_key=True)
    title = Column('title', String)
    link = Column('link', String)
    location = Column('location', String)
    description = Column('description', String)
    source = Column('source', String)  # where we take data from

    # if the jobs is created by company this will be 1 otherwise, it will be 0
    sponsor = Column('sponsor', Integer, nullable=True)
    company_name = Column('company_name', String, nullable=True)
    expire_day = Column('expire_day', DateTime, nullable=True)