# models/place_amenity.py
from sqlalchemy import Table, Column, String, ForeignKey
from models.base_model import Base

place_amenity = Table('place_amenity', Base.metadata,
    Column('place_id', String(60), ForeignKey('places.id', ondelete='CASCADE'), primary_key=True),
    Column('amenity_id', String(60), ForeignKey('amenities.id', ondelete='CASCADE'), primary_key=True)
)
