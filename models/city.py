#!/usr/bin/python3
"""Module for the City class."""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from os import environ
from uuid import uuid4

storage_env_variable = "HBNB_TYPE_STORAGE"

if storage_env_variable in environ.keys() and environ[storage_env_variable] == "db":
    class City(BaseModel, Base):
        '''
        City class to store city information.
        '''
        __tablename__ = "cities"
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        name = Column(String(128), nullable=False)
        places = relationship("Place", backref="cities", cascade="all,delete")

        def __init__(self, **kwargs):
            setattr(self, "id", str(uuid4()))
            for i, j in kwargs.items():
                setattr(self, i, j)
else:
    class City(BaseModel):
        '''
        City class to store city information.
        '''
        state_id = ""
        name = ""
