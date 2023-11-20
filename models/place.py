#!/usr/bin/python3

"""This module defines the Place class which inherit from the
BaseModel class and is a representation of a place (house/room)
rented by a host
"""

from models.base_model import BaseModel


class Place(BaseModel):
    """ Place: is the data representation of a Place object
    and is a place rented by a host on the airbnb_clone  app

    Attributes:
        `city_id` (str): is the identifier of the city, the place (house/room)
            is located in (City.id)
        `state_id` (str): is the identifier of the state, the place
            (house/room) is located in (State.id)
        `name` (str): is the name of the place
        `description` (str): is a short description of the place
        `number_rooms` (int): is a number of the rooms available in
            the place (house)
        `number_bathrooms` (int): number of the bathrooms available
            in the place (house)
        `max_guest` (int): is the maximum number of guests a place
            can accommodate
        `price_by_night` (int): is what a night at this place will cost
        `latitude` (float): is the latitude of the place
        `longitude` (float): is the longitude of the place
        `amenity_ids` (list[str]): is the list of the ids of
            available amenities

    """
    city_id: str = ""
    user_id: str = ""
    name: str = ""
    description: str = ""

    number_rooms: int = 0
    number_bathrooms: int = 0
    max_guest: int = 0
    price_by_night: int = 0

    latitude: float = 0.0
    longitude: float = 0.0

    amenity_ids: list = []
