#!/usr/bin/python3
<<<<<<< HEAD

"""This module creates a unique FileStorage instance
for application, when it is launched
"""

from models.engine.file_storage import FileStorage


# Creating a new empty FileStorage object
storage = FileStorage()

# Loading the data from the previous session
=======
"""__init__ magic method for models directory"""
from models.engine.file_storage import FileStorage


storage = FileStorage()
>>>>>>> 624c6c7a1feb5c89f440439f27954b2468ddfb3d
storage.reload()
