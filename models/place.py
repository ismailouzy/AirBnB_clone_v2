#!/usr/bin/python3
"""Module for the Place class"""

from property_models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer, Float, Table
from sqlalchemy.orm import relationship
from os import environ
from uuid import uuid4

place_amenity = Table(
    'place_amenity',
    Base.metadata,
    Column(
        'place_id',
        String(60),
        ForeignKey('places.id'),
        nullable=False),
    Column(
        'amenity_id',
        String(60),
        ForeignKey('amenities.id'),
        nullable=False))

storage_type = "PROPERTY_STORAGE_TYPE"
if storage_type in environ.keys() and environ["PROPERTY_STORAGE_TYPE"] == "db":
    class Place(BaseModel, Base):
        """Class for Place"""
        __tablename__ = "places"
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        reviews = relationship("Review", backref="place")
        amenities = relationship("Amenity",
                                 secondary=place_amenity, viewonly=False)

        def __init__(self, **kwargs):
            """Initialization method"""
            setattr(self, "id", str(uuid4()))
            for key, value in kwargs.items():
                setattr(self, key, value)
else:
    class Place(BaseModel):
        """Class for Place"""
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            """Property to retrieve reviews associated with Place"""
            all_reviews = property_models.storage.all(Review)
            liste = []
            for key, value in all_reviews.items():
                if "Review" == key[0:4] and value.place_id == self.id:
                    liste.append(value)
            return liste
