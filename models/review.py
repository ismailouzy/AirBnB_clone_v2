#!/usr/bin/python3
"""Module for the Review class"""

from property_models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer, Float, Table
from sqlalchemy.orm import relationship
from os import environ
from uuid import uuid4

storage_type = "PROPERTY_STORAGE_TYPE"
if storage_type in environ.keys() and environ["PROPERTY_STORAGE_TYPE"] == "db":
    class Review(BaseModel, Base):
        """Class for Review"""
        __tablename__ = "reviews"
        text = Column(String(1024), nullable=False)
        place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)

        def __init__(self, **kwargs):
            """Initialization method"""
            setattr(self, "id", str(uuid4()))
            for key, value in kwargs.items():
                setattr(self, key, value)
else:
    class Review(BaseModel):
        """Class for Review"""
        place_id = ""
        user_id = ""
        text = ""
