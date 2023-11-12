#!/usr/bin/python3

"""This module defines the State class which inherit from the
BaseModel class and is a representation of a State in which
a place (house/room) may be located
"""

from models.base_model import BaseModel


class State(BaseModel):
    """State: is the data representation of a State object
    and is a state in which a place is located

    Attributes:
        `name` (str): name of the state
    """
    name: str = ""
