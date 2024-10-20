""" This module contains the models for the elements table.
"""
from app.config import settings

from .base import BaseElement

# Constants
#: Default URI
DEFAULT_URI = settings.db.uri
#: Default database
DEFAULT_DB = "vidimost"
#: Default collection
DEFAULT_COLLECTION = 'elements'
# // Constants


class Element(BaseElement):
    """ An element in the database.
    """
    def __init__(self, 
                 code, 
                 value, 
                 date=None, 
                 label="", 
                 uri=DEFAULT_URI, 
                 dbname=DEFAULT_DB,
                 collection=DEFAULT_COLLECTION):
        super().__init__(uri, dbname, collection)
        self.date  = date
        self.code  = code
        self.label = label
        self.value = value

    def to_dict(self):
        return {"date": self.date,
                "code": self.code,
                "label": self.label,
                "value": self.value}

    @classmethod
    def from_dict(cls, data):
        return cls(date=data["date"],
                   code=data["code"],
                   label=data["label"],
                   value=data["value"])

    def __str__(self):
        return f"{self.code} - {self.label} ({self.date}): {self.value}"
