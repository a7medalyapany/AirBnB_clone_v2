#!/usr/bin/python3
"""Module for managing a MySQL database engine"""

import os
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


class DBStorage:
    """Manages a MySQL database storage system"""

    all_classes = {"BaseModel": BaseModel, "User": User, "State": State,
                   "City": City, "Amenity": Amenity, "Place": Place,
                   "Review": Review}
    __engine = None
    __session = None

    def __init__(self):
        """Initialize and configure the database"""
        self.__engine = create_engine(
            f"mysql+mysqldb://{os.environ['HBNB_MYSQL_USER']}:{os.environ['HBNB_MYSQL_PWD']}@{os.environ['HBNB_MYSQL_HOST']}/{os.environ['HBNB_MYSQL_DB']}",
            pool_pre_ping=True)
        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Retrieve all objects from the database session"""
        obj_dict = {}
        cls = self.all_classes.get(cls)
        if cls:
            objects = self.__session.query(cls).all()
        else:
            objects = self.__session.query(
                State, City, User, Amenity, Place, Review).all()
        for obj in objects:
            key = f"{obj.__class__.__name__}.{obj.id}"
            obj_dict[key] = obj
        return obj_dict

    def new(self, obj):
        """Add an object to the session"""
        self.__session.add(obj)
        self.__session.flush()

    def save(self):
        """Commit changes to the database"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete an object from the session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create database tables and reload session"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Close the current session"""
        self.__session.close()
