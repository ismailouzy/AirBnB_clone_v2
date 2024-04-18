#!/usr/bin/python3
"""File storage class for the AirBnB application."""

import os
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from models.base_model import Base

class DBStorage:
    """Class for database storage handling."""

    __engine = None
    __session = None
    valid_classes = ["User", "State", "City", "Amenity", "Place", "Review"]

    def __init__(self):
        """Initialize database storage."""
        self.__engine = create_engine("mysql+mysqldb://" +
                                      os.environ['HBNB_MYSQL_USER'] +
                                      ":" + os.environ['HBNB_MYSQL_PWD'] +
                                      "@" + os.environ['HBNB_MYSQL_HOST'] +
                                      ":3306/" +
                                      os.environ['HBNB_MYSQL_DB'])

        try:
            if os.environ['HBNB_MYSQL_ENV'] == "test":
                Base.metadata.drop_all(self.__engine)
        except KeyError:
            pass

    def all(self, cls=None):
        """Query all objects in the database."""
        storage = {}
        if cls is None:
            for cls_name in self.valid_classes:
                for instance in self.__session.query(eval(cls_name)):
                    storage[instance.id] = instance
        else:
            if cls not in self.valid_classes:
                return
            for instance in self.__session.query(eval(cls)):
                storage[instance.id] = instance

        return storage

    def new(self, obj):
        """Add an object to the database."""
        self.__session.add(obj)

    def save(self):
        """Save changes to the database."""
        try:
            self.__session.commit()
        except:
            self.__session.rollback()
            raise
        finally:
            self.__session.close()

    def update(self, cls, obj_id, key, new_value):
        """Update an object's attribute."""
        res = self.__session.query(eval(cls)).filter(eval(cls).id == obj_id)

        if res.count() == 0:
            return 0

        res.update({key: (new_value)})
        return 1

    def reload(self):
        """Create all tables and open session."""
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(sessionmaker(bind=self.__engine))

    def delete(self, obj=None):
        """Delete an object from the database."""
        if obj is None:
            return

        self.__session.delete(obj)

    def close(self):
        """Close the session."""
        self.__session.remove()
