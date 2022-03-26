import os
from time import time
from typing import List

from pymongo import MongoClient
from pymongo.cursor import Cursor

DB_HOST = os.environ.get("PIG_INSPECTIONS_DB_HOST")
DB_PORT = os.environ.get("PIG_INSPECTIONS_DB_PORT")
DB_USER = os.environ.get("PIG_INSPECTIONS_DB_USER")
DB_PASS = os.environ.get("PIG_INSPECTIONS_DB_PASS")
DB_NAME = os.environ.get("PIG_INSPECTIONS_DB_NAME")


class DatabaseClient:
    def __init__(self, collection_name):
        """Init

        :param collection_name: collection's name in the database where operations will be made
        """
        self._db_client = MongoClient(
            host=f"mongodb://{DB_USER}:{DB_PASS}@{DB_HOST}", port=DB_PORT
        )
        self._database = self._db_client[DB_NAME]
        self._collection = self._database[collection_name]

    def save(self, document: dict):
        """Save (create) a document on database

        :param document: document content
        """
        document["created_at"] = round(time())
        document["updated_at"] = round(time())
        return self._collection.insert_one(document)

    def update(self, document: dict, query: dict = dict()):
        """Update a existing document on database

        :param document: document content
        :param query: a dictionary specifying the query to found the
            document that will be replaced
        """
        document["updated_at"] = round(time())
        return self._collection.replace_one(query, document)

    def save_list(self, document_list: List[dict] = []):
        """Save a list of documents

        :param document_list (list<dict>): list of documents that should be saved
        """
        for document in document_list:
            self.save(document)

    def get(self, query: dict, fields: set = None):
        """Retrieve a Document from database

        :param query: a dictionary specifying the query to found the document
        :param fields: a set specifying the fields of document to be returned
        """
        return self._collection.find_one(filter=query, projection=fields)

    def get_list(self, query: dict = {}, fields=None) -> Cursor:
        """Retrieve a Document from database

        :param query (optional): a dictionary specifying the query to found the documents
        :param fields: a set specifying the fields of documents to be returned
        """
        return self._collection.find(filter=query, projection=fields)

    def count(self, query: dict = {}):
        """Counts the number of documents in a collection

        :param query (optional): a dictionary specifying the query to found the documents
        """
        return self._collection.count(query)
