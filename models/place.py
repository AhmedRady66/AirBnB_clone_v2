#!/usr/bin/python3
""" Place Module for HBNB project """
from os import getenv
from sqlalchemy import Column, String, ForeignKey, Integer, Float, Table
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from models.review import Review
from models.amenity import Amenity
import models

create_table = Table('place_amenity', Base.metadata,
                     Column('place_id', String(60), ForeignKey('places.id'),
                            primary_key=True, nullable=False),
                     Column('amenity_id', String(60),
                            ForeignKey('amenities.id'),
                            primary_key=True, nullable=False))


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
    amenities = relationship("Amenity",
                             secondary="place_amenity", viewonly=False)
    amenity_ids = []

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        reviews = relationship("Review", backref="place")

    else:
        @property
        def reviews(self):
            """returns the list of Review instances with place_id"""
            review_list = []
            all_reviews = models.storage.all(Review)
            for review in all_reviews.values():
                if review.place_id == self.id:
                    review_list.append(review)
            return review_list

        @property
        def amenities(self):
            """returns the list of Amenity instances"""
            amenitie_list = []
            all_amenities = models.storage.all(Amenity)
            for amenitie in all_amenities.values():
                if amenitie.place_id == self.id:
                    amenitie_list.append(amenitie)
            return amenitie_list

        @amenities.setter
        def amenities(self, value):
            """set value to amenities"""
            if isinstance(value, Amenity):
                self.amenity_ids.append(value)
