from db_schema import User,Wikipage
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
import dbservice

db_url = "sqlite:///wiki.db"
engine = create_engine(db_url, connect_args={'check_same_thread': False})

Session = sessionmaker(bind=engine)
session = Session()

def get_user_by_name( name ):
    user = session.query(User).filter( User.username == name ).one()
    return user

def get_user_by_id( user_id ):
    user = session.query(User).filter( User.id == user_id ).one()
    return user

def get_wikipage_by_title( page_title ):
    page = session.query(Wikipage).filter(Wikipage.title == page_title).one()
    return page

def get_all_users():
    all_users = session.query(User).all()
    return all_users

def get_all_wikipages():
    all_pages = session.query(Wikipage).all()
    return all_pages

def create_wikipage( title, content, owner):
    new_page = Wikipage( title = title , content = content, owner = owner.id )
    session.add( new_page )
    session.commit()
