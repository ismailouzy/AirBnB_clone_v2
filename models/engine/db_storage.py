#!/usr/bin/python3
"""File storage class for the AirBnB"""
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy import create_engine
from property_models import *


class PropertyStorage:
    """
    This class manages the database storage for the property rental system.
    """

    __engine = None
    __session = None
    valid_classes = ["User", "State", "City", "Amenity", "Place", "Review"]

    def __init__(self):
        """
        Initializes PropertyStorage class with database connection details.
        """
        self.__engine = create_engine("mysql+mysqldb://" +
                                      os.environ['PROPERTY_MYSQL_USER'] +
                                      ":" + os.environ['PROPERTY_MYSQL_PWD'] +
                                      "@" + os.environ['PROPERTY_MYSQL_HOST'] +
                                      ":3306/" +
                                      os.environ['PROPERTY_MYSQL_DB'])

        try:
            if os.environ['PROPERTY_MYSQL_ENV'] == "test":
                Base.metadata.drop_all(self.__engine)
        except KeyError:
            pass

    def all(self, cls=None):
        """
        Retrieves all objects of a specified class from the database.

        Args:
            cls (str): Optional. Class name of the objects to retrieve.

        Returns:
            dict: A dictionary containing objects keyed by their IDs.
        """
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
        """
        Adds a new object to the current database session.

        Args:
            obj: The object to add to the session.
        """
        self.__session.add(obj)

    def save(self):
        """
        Commits changes to the database session.
        """
        self.__session.commit()

    def update(self, cls, obj_id, key, new_value):
        """
        Updates an object's attribute in the database.

        Args:
            cls (str): The class name of the object.
            obj_id (str): The ID of the object.
            key (str): The attribute to update.
            new_value: The new value of the attribute.

        Returns:
            int: 1 if successful, 0 otherwise.
        """
        res = self.__session.query(eval(cls)).filter(eval(cls).id == obj_id)

        if res.count() == 0:
            return 0

        res.update({key: (new_value)})
        return 1

    def reload(self):
        """
        Reloads the database session.
        """
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(sessionmaker(bind=self.__engine))

    def delete(self, obj=None):
        """
        Deletes an object from the database session.

        Args:
            obj: The object to delete.
        """
        if obj is None:
            return

        self.__session.delete(obj)

    def close(self):
        """
        Closes the database session.
        """
        self.__session.remove()
