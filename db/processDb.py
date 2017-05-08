"""
processDb : SQLAlchemy example by ORM usage

Author : VinceDgy

see : https://www.sqlalchemy.org/

Warning : don't forget to install requirements first
$ pip install -r requirements.txt

The test database is launched with a docker container that runs locally
Please check out the directory 'docker' and launch with within another terminal
$ cd ./docker
$ docker-compose up

"""
from __future__ import print_function
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import logging
import csv
import os
from datetime import datetime

# Define log
logging.basicConfig(
    level=getattr(logging, 'DEBUG'),
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    filename=os.path.join(os.path.dirname(__file__), os.path.basename(__file__)+'.log'),
    filemode='a'
)

# Create Connection to database
URL = 'mysql+mysqldb://root:rpass@127.0.0.1:3306/mydb'
VERBOSE = False

# ORM Mapping engine
BASE = declarative_base()


class User(BASE):
    """ User """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    fullname = Column(String(256))
    password = Column(String(256))
    addresses = relationship("Address", back_populates='user',
                             cascade="all, delete, delete-orphan")

    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (
            self.name, self.fullname, self.password)

class Address(BASE):
    """ Address """
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    email_adress = Column(String(256), nullable=False)
    user_id = Column(None, ForeignKey('users.id'))
    user = relationship("User", back_populates="addresses")

    def __repr__(self):
        return "<Address(user_id='%s', fullname='%s')>" % (
            self.name, self.fullname)

# ======================================================================
# Main program
# ======================================================================
if __name__ == '__main__':
    # Create tables
    ENGINE = create_engine(URL, echo=VERBOSE, pool_recycle=10)
    BASE.metadata.create_all(ENGINE)
    # Create a session
    SESSION = sessionmaker(bind=ENGINE)()
    # Insert few users in ddb
    USER = User(name='ed', fullname='Ed Jones', password='edspassword')
    SESSION.add(USER)
    OUR_USER = SESSION.query(User).filter_by(name='ed').first()
    logging.info(OUR_USER)
    # Adding more Users
    SESSION.add_all([
        User(name='wendy', fullname='Wendy Williams', password='foobar'),
        User(name='mary', fullname='Mary Contrary', password='xxg527'),
        User(name='fred', fullname='Fred Flinstone', password='xxx')])
    SESSION.commit()

    # Load a big amount of rows from the file
    print("Bulk Load ")
    ROWSIZE=50000
    
    # Bulk Load
    Users = []
    with open(os.path.join(os.path.dirname(__file__), 'data.csv'), 'rb') as csvfile:
        READER = csv.reader(csvfile, delimiter=',')
        HEADER = READER.next()
        for idx, row in enumerate(READER):
            Users.append(User(name=row[0], fullname=row[1], password=row[2]))
            if idx%ROWSIZE == 0:
                SESSION.bulk_save_objects(Users)
                SESSION.commit()
                Users=[]
        SESSION.bulk_save_objects(Users)
    SESSION.commit()

    # Select all users
    #CONNECTION = ENGINE.connect()
    #for row in CONNECTION.execute("select fullname from users"):
    #    print("username:'%s" % (row['fullname']))
    # Delete all Users
    #for instance in SESSION.query(User).order_by(User.id):
    #    print("Deleting user '%s'" % (instance.fullname))
    #    SESSION.delete(instance)
    #SESSION.commit()
    # Drop tables
    # User.__table__.drop(ENGINE)
    # Address.__table__.drop(ENGINE)
    # Close Connection
    #CONNECTION.close()
