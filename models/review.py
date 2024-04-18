#!/usr/bin/python3
"""Module for the Review class."""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from os import environ
from uuid import uuid4

storage_env_variable = "HBNB_TYPE_STORAGE"

if storage_env_variable in environ.keys() and environ[storage_env_variable] == "db":
    class Review(BaseModel, Base):
        """Class for Review representation."""
        __tablename__ = "reviews"
        text = Column(String(1024), nullable=False)
        place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)

        def __init__(self, **kwargs):
            """Initialization of Review."""
            setattr(self, "id", str(uuid4()))
            for i, j in kwargs.items():
                setattr(self, i, j)
else:
    class Review(BaseModel):
        """Class for Review representation."""
        place_id = ""
        user_id = ""
        text = ""
