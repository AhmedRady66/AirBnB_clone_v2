#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, String
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
import models


class Amenity(BaseModel, Base):
    """amenities Database class"""
    __tablename__ = 'amenities'
    name = Column(String(128), nullable=False)
    place_amenities = relationship('Place', secondary='place_amenity', viewonly=True)
