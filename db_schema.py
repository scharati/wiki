from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Column
from sqlalchemy import Table
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import Text
from sqlalchemy import UniqueConstraint

from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

engine = create_engine("sqlite:///wiki.db")

Base = declarative_base()

""" The User Model """
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True )
    username = Column(Text(100), nullable=False)
    pwdhash = Column(String(300), nullable=False)
    __table_args__ = (
        (UniqueConstraint('username'),)
    )

""" The Wikipage Model """
class Wikipage(Base):
    __tablename__ = "wikipages"
    id = Column(Integer, primary_key=True)
    title = Column(Text(300) )
    content = Column(Text)
    owner = Column(Integer, ForeignKey( "users.id" ))
    __table_args__ = (
        (UniqueConstraint('title'),)
    )

Base.metadata.create_all(engine)
# Base.metadata.drop_all(engine)