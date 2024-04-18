#!/usr/bin/python3
"""Module for the City class"""
from property_models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from os import environ
from uuid import uuid4

storage_type = "PROPERTY_STORAGE_TYPE"
if storage_type in environ.keys() and environ["PROPERTY_STORAGE_TYPE"] == "db":
    class City(BaseModel, Base):
        '''
        Class defining City attributes
        '''
        __tablename__ = "cities"
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        name = Column(String(128), nullable=False)
        places = relationship("Place", backref="cities", cascade="all,delete")

        def __init__(self, **kwargs):
            setattr(self, "id", str(uuid4()))
            for key, value in kwargs.items():
                setattr(self, key, value)
else:
    class City(BaseModel):
        '''
        Class for City
        '''
        state_id = ""
        name = ""
