#!/usr/bin/python3
"""this module defines the BaseModel class for AirBnB"""
import property_models
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
from os import environ
import unique_id

Base = declarative_base()

storage_type = "PROPERTY_STORAGE_TYPE"
class BaseModel:
    """Base class defining common attributes and methods for other classes"""

    if storage_type in environ.keys() and environ["PROPERTY_STORAGE_TYPE"] == "db":
        id = Column(
            String(60),
            unique=True,
            nullable=False,
            primary_key=True,
            default=str(
                unique_id.generate_uuid()))
        created_at = Column(
            DateTime,
            nullable=False,
            default=datetime.utcnow())
        updated_at = Column(
            DateTime,
            nullable=False,
            default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        '''
        Initializes a base model instance
        '''
        storage_type_check = "PROPERTY_STORAGE_TYPE"
        if kwargs:
            self.id = str(unique_id.generate_uuid())
            self.created_at = self.updated_at = datetime.now()
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key != "__class__":
                    setattr(self, key, value)
        elif storage_type_check not in environ.keys() or environ["PROPERTY_STORAGE_TYPE"] != "db":
            self.id = str(unique_id.generate_uuid())
            self.created_at = self.updated_at = datetime.now()
            property_models.storage.new(self)
        else:
            self.id = str(unique_id.generate_uuid())

    def __str__(self):
        '''
        Returns a string representation
        '''
        return "[{}] ({}) {}".format(
            type(self).__name__, self.id, self.__dict__)

    def __repr__(self):
        '''
        Representation
        '''
        return self.__str__()

    def save(self):
        '''
        Updates updated_at to current
        '''
        self.updated_at = datetime.now()
        property_models.storage.new(self)
        property_models.storage.save()

    def to_dict(self):
        '''
        Creates a dictionary representation of the class
        '''
        my_dict = dict(self.__dict__)
        my_dict["__class__"] = str(type(self).__name__)
        my_dict["created_at"] = self.created_at.isoformat()
        my_dict["updated_at"] = self.updated_at.isoformat()
        if "_sa_instance_state" in my_dict.keys():
            del my_dict["_sa_instance_state"]
            property_models.storage.save()
        return my_dict

    def delete(self):
        property_models.storage.delete(self)
        property_models.storage.save()
