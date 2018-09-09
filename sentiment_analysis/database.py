import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


try:
    from config import DATABASE_URL
except:
    from configdist import DATABASE_URL


class BaseEntity(object):
    """Base class for all database Entitys"""

    @classmethod
    def count(cls):
        return len(cls.all())

    @classmethod
    def all(cls):
        """Get all Entities"""
        return cls.query.all()

    @classmethod
    def get(cls, id):
        """Get an Entity by it's PK"""
        return cls.query.filter(cls.id == id).first()

    @classmethod
    def get_by_ids(cls, id_list):
        """Get a list of Entities by their PK"""
        if len(id_list) == 0:
            return []
        return cls.query.filter(cls.id.in_(id_list)).all()

    def save(self, commit=True):
        """Creates or updates an Entity in the database"""
        db_session.add(self)
        if commit:
            db_session.commit()

    def delete(self, commit=True):
        """Removes an Entity from the database"""
        db_session.delete(self)
        if commit:
            db_session.commit()


# Create declarative base Entity for database objects
Entity = declarative_base(name="Entity", cls=BaseEntity)

# Create database engine
engine = create_engine(DATABASE_URL, convert_unicode=True)

# Create our scoped database session and bind to the engine
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
# Attach database session to all Entitys
Entity.db_session = db_session

# Attach query property to all Entitys
Entity.query = db_session.query_property()
