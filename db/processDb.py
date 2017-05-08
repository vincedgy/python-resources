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
from sqlalchemy.orm import sessionmaker
import logging

# Define log
logging.basicConfig(
        level=getattr(logging, 'DEBUG'),
        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p',
        filename='processDb.log',
        filemode='a'
        )

# Create Connection to database
URL = 'mysql+mysqldb://root:rpass@127.0.0.1:3306/mydb'

# ORM Mapping engine
BASE = declarative_base()

class User(BASE):
    """ User """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    fullname = Column(String(256))
    password = Column(String(256))

    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (
            self.name, self.fullname, self.password)

class Addresses(BASE):
    """ Addresses """
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    user_id = Column(None, ForeignKey('users.id'))
    fullname = Column(String(256), nullable=False)

    def __repr__(self):
        return "<Address(user_id='%s', fullname='%s')>" % (
            self.name, self.fullname)

# ======================================================================
# Main program
# ======================================================================
if __name__ == '__main__':
    # Create tables
    ENGINE = create_engine(URL, echo=True, pool_recycle=3600)
    BASE.metadata.create_all(ENGINE)
    # Create a session
    SESSION = sessionmaker(bind=ENGINE)()
    # Insert few users in ddb
    USER = User(name='ed', fullname='Ed Jones', password='edspassword')
    SESSION.add(USER)
    SESSION.commit()
    OUR_USER = SESSION.query(User).filter_by(name='ed').first()
    print(OUR_USER)
    # Select all users
    CONNECTION = ENGINE.connect()
    for row in CONNECTION.execute("select fullname from users"):
        print("username:", row['fullname'])
    CONNECTION.close()
