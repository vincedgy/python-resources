"""
processDb : 
"""
from __future__ import print_function
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey
import pdb

# Create SQLLite engine
engine = create_engine('sqlite:///:memory:', echo=True)

# Create table 
metadata = MetaData()

def create_tables():
    """ create_tables """
    users = Table('users', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('name', String),
                    Column('fullname', String), 
                    Column('secret', String)
                )
    addresses = Table('addresses', metadata,
        Column('id', Integer, primary_key=True),
        Column('user_id', None, ForeignKey('users.id')),
        Column('email_address', String, nullable=False)
    )
    metadata.create_all(engine)
    ins = users.insert()
    print(ins)


