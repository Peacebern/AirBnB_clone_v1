#!/usr/bin/python3
""" Place Module for HBNB project """
from os import getenv
import models
from os import getenv
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer, Float, Table
from sqlalchemy.orm import relationship
from models.review import Review
from models.amenity import Amenity


metadata = Base.metadata
place_amenity = Table('place_amenity', metadata,
                      Column('place_id', String(60), ForeignKey("places.id"),
                             primary_key=True, nullable=False),
                      Column('amenity_id', String(60), ForeignKey(
                             "amenities.id"), primary_key=True,
                             nullable=False))


class Place(BaseModel, Base):
    """ Attributes for place class"""
    __tablename__ = "places"

    city_id = Column(String(60),  ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []
    if getenv("HBNB_TYPE_STORAGE") == 'db':
        reviews = relationship('Review', backref='place',
                               cascade='all, delete-orphan')
        amenities = relationship('Amenity', secondary=place_amenity,
                                 backref="place_amenities",
                                 viewonly=False)

    if getenv("HBNB_TYPE_STORAGE") != 'db':
        @property
        def reviews(self):
            """returns list of review instances"""
            reviewList = []
            for reviews in models.storage.all(Review).values():
                if reviews.place_id == self.id:
                    reviewList.append(reviews)
            return reviewList

        @property
        def amenities(self):
            """returns list of amenity instances"""
            amenityList = []
            for amenities in models.storage.all(Amenity).values():
                if amenities.place_id == self.id:
                    amenityList.append(amenities)
            return amenityList

        @amenities.setter
        def amenities(self, amenityObject):
            if isinstance(amenityObject, Amenity):
                self.amenity_ids.append(amenityObject.id)
