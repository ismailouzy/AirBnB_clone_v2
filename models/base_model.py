#!/usr/bin/python3
"""This module defines the BaseModel class for a housing rental application."""
import models
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
from os import environ
import uuid

Base = declarative_base()

storage_env_variable = "HBNB_TYPE_STORAGE"


class BaseModel:
    """BaseModel class for common attributes/methods shared by other classes."""

    if storage_env_variable in environ.keys() and environ[storage_env_variable] == "db":
        id = Column(
            String(60),
            unique=True,
            nullable=False,
            primary_key=True,
            default=str(
                uuid.uuid4()))
        created_at = Column(
            DateTime,
            nullable=False,
            default=datetime.utcnow())
        updated_at = Column(
            DateTime,
            nullable=False,
            default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """
        Initializes an instance of BaseModel.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        env_var = "HBNB_TYPE_STORAGE"
        if kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.now()
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key != "__class__":
                    setattr(self, key, value)
        elif env_var not in environ.keys() or environ[env_var] != "db":
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.now()
            models.storage.new(self)
        else:
            self.id = str(uuid.uuid4())

    def __str__(self):
        """
        Returns a string representation of the object.

        Returns:
            str: String representation.
        """
        return "[{}] ({}) {}".format(
            type(self).__name__, self.id, self.__dict__)

    def __repr__(self):
        """
        Returns a string representation of the object.

        Returns:
            str: String representation.
        """
        return self.__str__()

    def save(self):
        """
        Updates updated_at to current datetime and saves the object.
        """
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """
        Returns a dictionary representation of the object.

        Returns:
            dict: Dictionary representation.
        """
        my_dict = dict(self.__dict__)
        my_dict["__class__"] = str(type(self).__name__)
        my_dict["created_at"] = self.created_at.isoformat()
        my_dict["updated_at"] = self.updated_at.isoformat()
        if "_sa_instance_state" in my_dict.keys():
            del my_dict["_sa_instance_state"]
            models.storage.save()
        return my_dict

    def delete(self):
        """Deletes the object from storage."""
        models.storage.delete(self)
        models.storage.save()
