#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import String, Column


class Amenity(BaseModel, Base):
    """class for amenities"""
    __tablename__ = 'amenities'
    name = Column(String(128), nullable=False)
