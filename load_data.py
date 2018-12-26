from db_schema import User,Wikipage
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
import encryptsha256

engine = create_engine("sqlite:///wiki.db")
# set up the Session class with default constructor arguments
Session = sessionmaker(bind=engine)
# create a session object of Session class with default constructor arguments
session = Session()

user1_pwhash = encryptsha256.make_hash("pw_user1")
user2_pwhash = encryptsha256.make_hash("pw_user2")

user1 = User( username="user1@hamsa.org", pwdhash=user1_pwhash)
user2 = User( username="user2@hamsa.org", pwdhash=user2_pwhash)


wikip1 = Wikipage( title = "Bharat", content = "Bharat is the native name of India", owner=user1.id)
wikip2 = Wikipage( title = "Karnataka", content = "<h1> Karnataka is a state in the southern part of india </h1>", owner=user2.id )

session.add(user1)
session.add(user2)

session.add(wikip1)
session.add(wikip2)

session.commit()