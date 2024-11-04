""" This module contains the base model for the database.
"""
import logging
from pymongo import MongoClient


class BaseElement:
    """ Base model for the database.
    """
    client     = None
    db         = None
    collection = None

    def __init__(self, uri, dbname, collection):
        """ Initialize the base model.

            Create a connection to the database.
        """
        self.uri              = uri
        self.db_name          = dbname
        self.collection_name  = collection

        self.connect(self.uri, 
                     self.db_name, 
                     self.collection_name)
    
    def connect(self, uri, dbname, collection, force=False):
        """ Connect to the database.
        """
        if self.client is None or force:
            self.client = MongoClient(uri)
            self.db     = self.client[dbname]
            self.collection = self.db[collection]
        else:
            logging.info("Already connected to the database.")

        return self.client, self.db, self.collection

    def close(self):
        """ Close the connection to the database.
        """
        self.client.close()

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
