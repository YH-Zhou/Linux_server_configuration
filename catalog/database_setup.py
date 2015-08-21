import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, deferred
from sqlalchemy import create_engine, LargeBinary, BLOB

Base = declarative_base()


class User(Base):
    """ Create User table to store user information """
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    picture = Column(String)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)


class Catalog(Base):
    """ Create Catalog table to store catalog information """
    __tablename__ = 'catalog'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    description = Column(String)
    #description = Column(Text)

# This serialize function is used to send JSON objects in a
# serializable format
    @property
    def serialize(self):
        return {
             'name': self.name,
             'id': self.id,
             'description': self.description
               }


class CatalogItem(Base):
    __tablename__ = 'catalog_item'

    name = Column(String, nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String)
    #description = Column(Text)
    catalog_id = Column(Integer, ForeignKey('catalog.id'))
    catalog = relationship(Catalog)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
             'name': self.name,
             'description': self.description,
             'id': self.id
               }

#engine = create_engine('sqlite:///catalogmenuwithusers.db')
engine = create_engine('postgresql://catalog:catalog@localhost/catalogmenu')

Base.metadata.create_all(engine)
