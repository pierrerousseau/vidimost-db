""" This module contains the base model for the database.
"""
import logging
from pymongo import MongoClient


class BaseElement:
    """ Base model for the database.
    """
    uri             = None
    db_name         = None
    collection_name = None

    client     = None
    db         = None
    collection = None

    def __init__(self, uri=None, db_name=None, collection_name=None):
        """ Initialize the base model.

            Create a connection to the database.
        """
        if uri is not None:
            self.uri = uri
        
        if db_name is not None:
            self.db_name = db_name
        
        if collection_name is not None:
            self.collection_name  = collection_name
    
    def to_dict(self):
        """ Convert to dictionnary.

            To be implemented at inheritance.
        """
    
    @classmethod
    def from_dict(cls, data):
        """ Convert to object.

            To be implemented at inheritance.
        """

    @classmethod
    def connect(cls, uri, dbname, collection, force=False):
        """ Connect to the database.
        """
        if cls.client is None or force:
            cls.client     = MongoClient(uri)
            cls.db         = cls.client[dbname]
            cls.collection = cls.db[collection]
        else:
            logging.info("Already connected to the database.")

        return cls.client, cls.db, cls.collection

    @classmethod
    def close(cls):
        """ Close the connection to the database.
        """
        cls.client.close()

    def insert(self):
        """ Insert one element in the collection.
        """
        if self.collection is None:
            self.connect(self.uri, self.db_name, self.collection_name)
        
        self.collection.insert_one(self.to_dict())

    def update(self, upsert=True):
        """ Update the element in the collection.
        """
        if self.collection is None:
            self.connect(self.uri, self.db_name, self.collection_name)
        
        self.collection.update_one({"code": self.code},
                                   {"$set": self.to_dict()}, 
                                   upsert=upsert)

    @classmethod
    def find_all(cls, query=None):
        """ Find all elements matching a query.
        """
        if cls.collection is None:
            cls.connect(cls.uri, cls.db_name, cls.collection_name)

        if query is None:
            query = {}
        
        elements = cls.collection.find(query)

        return (cls.from_dict(element) for element in elements)
