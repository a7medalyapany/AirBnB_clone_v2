#!/usr/bin/python3
"""Defines the State class"""

import os
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """Represents a state"""

    __tablename__ = 'states'

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        name = Column(String(128), nullable=False)
        cities = relationship(
            'City', back_populates='state',
            cascade='all, delete, delete-orphan')

    else:
        name = ""

        @property
        def cities(self):
            """Returns a list of associated City instances"""
            city_instances = []
            city_dict = models.storage.all(models.City)
            for key, value in city_dict.items():
                if self.id == value.state_id:
                    city_instances.append(value)
            return city_instances
