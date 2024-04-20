#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from models.city import City
from models.user import User


place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60), ForeignKey('places.id'),
                             primary_key=True, nullable=False),
                      Column('amenity_id', String(60),
                             ForeignKey('amenities.id'), primary_key=True,
                             nullable=False)
                      )


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
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
    amenities = relationship("Amenity", secondary=place_amenity,
                             viewonly=False)

    @property
    def reviews(self):
        """ reviews """
        dict_rev = models.storage.all(models.Review)
        list_rev = []
        for review in dict_rev.values():
            if review.place_id == self.id:
                list_reviews.append(review)

        return review

    @property
    def amenities(self):
        """Getter attribute that returns the list of Amenity instances based on
        the attribute amenity_ids that contains all Amenity.id linked to the
        Place.
        """
        from models import storage
        my_list = []
        extracted_amenities = storage.all('Amenity').values()
        for amenity in extracted_amenities:
            if self.id == amenity.amenity_ids:
                my_list.append(amenity)
        return my_list

    @amenities.setter
    def amenities(self, obj):
        """Setter attribute that handles append method for adding an Amenity.id
        to the attribute amenity_ids.
        """
        if isinstance(obj, 'Amenity'):
            self.amenity_id.append(obj.id)
