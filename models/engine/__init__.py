#!/usr/bin/python3

"""This module creates a unique FileStorage instance
for the application, when it is launched
"""

from models.engine.file_storage import FileStorage


# Creating a new empty FileStorage object
storage = FileStorage()

# Loading the data from the previous session
storage.reload()
