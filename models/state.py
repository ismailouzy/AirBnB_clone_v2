#!/usr/bin/python3
# Module for the State class.

import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv

class State(BaseModel, Base):
    """State class for storing state information."""
    __tablename__ = "states"
    name = Column(String(128), nullable=False)

    cities = relationship("City", backref="state", cascade="all, delete, delete-orphan")

    def __init__(self, *args, **kwargs):
        """Initializes an instance of State."""
        super().__init__(*args, **kwargs)

    if getenv('HBNB_TYPE_STORAGE', '') != 'db':
        @property
        def cities(self):
            """Property getter for cities."""
            all_cities = models.storage.all("City")
            temp = []
            for c_id in all_cities:
                if all_cities[c_id].state_id == self.id:
                    temp.append(all_cities[c_id])

            return temp
