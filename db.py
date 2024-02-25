from pymongo import MongoClient
from typing import Optional, Dict, Union, List, Tuple


class IVOverflowDB:
    """
    IVOverflowDB provides MongoDB database access methods for the IVOverflow API.
    """

    def __init__(self):
        """
        Initializes IVOverflowDB with a MongoDB client connected to the 'IVOverflow' database.
        """
        self.client = MongoClient('mongodb://localhost:27017')
        self.db = self.client['IVOverflow']

    @staticmethod
    def get_db():
        """
        Static method to get an instance of the IVOverflowDB class.

        Returns:
            IVOverflowDB: An instance of the IVOverflowDB class.
        """
        return IVOverflowDB()

    def create_document(self, collection_name: str, document_data: Dict[str, Union[int, str, dict]]) -> str:
        """
        Creates a new document in the specified collection.

        Args:
            collection_name (str): The name of the MongoDB collection.
            document_data (Dict): The data for the new document.

        Returns:
            str: The ObjectId of the newly inserted document.
        """
        collection = self.db[collection_name]
        result = collection.insert_one(document_data)
        return str(result.inserted_id)

    def get_document(
            self,
            collection_name: str,
            field_name: str = None,
            field_value: Union[int, str, dict] = None
    ) -> Optional[Dict[str, Union[int, str, dict]]]:
        """
        Retrieves a single document from the specified collection based on a field and its value.

        Args:
            collection_name (str): The name of the MongoDB collection.
            field_name (str): The name of the field to query.
            field_value (Union[int, str, dict]): The value to match in the specified field.

        Returns:
            Optional[Dict]: The retrieved document as a dictionary or None if not found.
        """
        collection = self.db[collection_name]
        document = collection.find_one({field_name: field_value}, projection={'_id': 0})
        return document

    def get_documents(
            self,
            collection_name: str,
            field_name: str = None,
            field_value: Union[int, str, dict] = None,
            sort: dict = None,
            skip: int = 0,
            limit: int = 0
    ) -> List[Dict[str, Union[dict, int, str]]]:
        """
        Retrieves a list of documents from the specified collection based on a field and its value, with optional sorting, skipping, and limiting.

        Args:
            collection_name (str): The name of the MongoDB collection.
            field_name (str): The name of the field to query.
            field_value (Union[int, str, dict]): The value to match in the specified field.
            sort (Optional[List[Tuple[str, int]]]): A list of tuples specifying sorting criteria.
            skip (int): The number of documents to skip.
            limit (int): The maximum number of documents to retrieve.

        Returns:
            List[Dict]: A list of retrieved documents as dictionaries.
        """
        collection = self.db[collection_name]

        query = {field_name: field_value} if field_name and field_value else {}
        cursor = collection.find(query, projection={'_id': 0})

        if sort:
            cursor = cursor.sort(sort)

        if skip:
            cursor = cursor.skip(skip)

        if limit:
            cursor = cursor.limit(limit)

        documents = list(cursor)
        return documents

    def update_document(self, collection_name: str, field_name: str, field_value: str, update_data: dict) -> int:
        """
        Updates a document in the specified collection based on a field and its value.

        Args:
            collection_name (str): The name of the MongoDB collection.
            field_name (str): The name of the field to query.
            field_value (str): The value to match in the specified field.
            update_data (dict): The data to update in the document.

        Returns:
            int: The number of documents modified (should be 1 in most cases).
        """
        collection = self.db[collection_name]
        filter_query = {field_name: field_value}
        result = collection.update_one(filter_query, {'$set': update_data})
        return result.modified_count

    def aggregate(self, collection_name: str, pipeline: list):
        """
        Performs an aggregation on the specified collection using the provided pipeline.

        Args:
            collection_name (str): The name of the MongoDB collection.
            pipeline (list): The aggregation pipeline.

        Returns:
            pymongo.command_cursor.CommandCursor: The result of the aggregation.
        """
        collection = self.db[collection_name]
        result = collection.aggregate(pipeline)
        return result
