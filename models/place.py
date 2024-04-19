#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from models.city import City
from models.user import User


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        place_amenity = Table(
            'place_amenity', Base.metadata,
            Column('place_id', String(60), ForeignKey('places.id'),
                   primary_key=True, nullable=False),
            Column('amenity_id', String(60), ForeignKey('amenities.id'),
                   primary_key=True, nullable=False)
        )
        amenities = relationship("Amenity", secondary=place_amenity)
    else:
        @property
        def amenities(self):
            """ Getter attribute for amenities in FileStorage """
            from models import storage
            from models.amenity import Amenity

            amenity_list = []
            for amenity in storage.all(Amenity).values():
                if amenity.id in self.amenity_ids:
                    amenity_list.append(amenity)
            return amenity_list

        @amenities.setter
        def amenities(self, obj=None):
            """ Setter attribute for amenities in FileStorage """
            if isinstance(obj, Amenity):
                self.amenity_ids.append(obj.id)

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

    # Define the relationships
    city = relationship("City", back_populates="places")
    user = relationship("User", back_populates="places")

    reviews = relationship("Review", cascade="delete", backref="place")

    @property
    def reviews(self):
        """ reviews """
        dict_rev = models.storage.all(models.Review)
        list_rev = []

        for review in dict_rev.values():
            if review.place_id == self.id:
                list_reviews.append(review)

        return review
