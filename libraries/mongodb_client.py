import os
from time import time
from typing import List, Optional

from bson.objectid import ObjectId
from pymongo import MongoClient
from pymongo.cursor import Cursor

DB_HOST = os.environ.get("PIG_INSPECTIONS_DB_HOST")
DB_PORT = int(os.environ.get("PIG_INSPECTIONS_DB_PORT", "27017"))
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

    def save(self, document: dict) -> Optional[str]:
        """Save (create) a document on database

        :param document: document content
        """
        document["created_at"] = round(time())
        document["updated_at"] = round(time())
        inserted_id = self._collection.insert_one(document).inserted_id
        if inserted_id:
            return str(inserted_id)
        return None

    def update(self, document: dict, query: dict) -> Optional[str]:
        """Update a existing document on database

        :param document: document content
        :param query: a dictionary specifying the query to found the
            document that will be replaced
        """
        query["_id"] = self._handle_id(query.get("_id"))
        document["updated_at"] = round(time())

        upserted_id = self._collection.update_one(query, {"$set": document}).upserted_id
        # upserted_id = self._collection.replace_one(
        #     query, document
        # ).upserted_id
        if upserted_id:
            return str(upserted_id)

        return None

    def save_list(self, document_list: List[dict] = []) -> None:
        """Save a list of documents

        :param document_list (list<dict>): list of documents that should be saved
        """
        self._collection.insert_many(document_list).inserted_ids

    def get(self, query: dict, fields: set = None) -> dict:
        """Retrieve a Document from database

        :param query: a dictionary specifying the query to found the document
        :param fields: a set specifying the fields of document to be returned
        """
        query["_id"] = self._handle_id(query.get("_id"))

        return self._collection.find_one(filter=query, projection=fields)

    def get_list(self, query: dict = {}, fields=None) -> Cursor:
        """Retrieve a Document from database

        :param query (optional): a dictionary specifying the query to found the documents
        :param fields: a set specifying the fields of documents to be returned
        """
        return self._collection.find(filter=query, projection=fields)

    def delete(self, query: dict, fields: set = None) -> dict:
        """Delete a Document

        :param query: a dictionary specifying the query to found the document
        :param fields: a set specifying the fields of document to be returned
        """
        query["_id"] = self._handle_id(query.get("_id"))
        self._collection.delete_one(filter=query)

    def count(self, query: dict = {}) -> int:
        """Counts the number of documents in a collection

        :param query (optional): a dictionary specifying the query to found the documents
        """
        return self._collection.count(query)

    def _handle_id(self, str_id: str):
        try:
            return ObjectId(str_id)
        except:
            return None
