from pymongo import MongoClient
from pymongo.collection import Collection
from typing import Optional, Dict, Union, List, Tuple
from bson import ObjectId


class IVOverflowDB:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017')
        self.db = self.client['IVOverflow']

    @staticmethod
    def get_db():
        return IVOverflowDB()

    def create_document(self, collection_name: str, document_data: Dict[str, Union[int, str, dict]]) -> str:
        collection = self.db[collection_name]
        result = collection.insert_one(document_data)
        return str(result.inserted_id)

    def get_document(
            self,
            collection_name: str,
            field_name: str = None,
            field_value: Union[int, str, dict] = None
    ) -> Optional[Dict[str, Union[int, str, dict]]]:
        collection = self.db[collection_name]
        document = collection.find_one({field_name: field_value})
        return document

    def get_documents(
            self,
            collection_name: str,
            field_name: str = None,
            field_value: Union[int, str, dict] = None,
            projection: Optional[Dict[str, Union[int, str]]] = None,
            sort: Optional[List[Tuple[str, int]]] = None,
            skip: int = 0,
            limit: int = 0
    ) -> List[Dict[str, Union[dict, int, str]]]:
        collection = self.db[collection_name]

        query = {field_name: field_value} if field_name and field_value else {}
        cursor = collection.find(query, projection=projection)

        if sort:
            cursor = cursor.sort(sort)

        if skip:
            cursor = cursor.skip(skip)

        if limit:
            cursor = cursor.limit(limit)

        documents = list(cursor)
        return documents

    def update_document(self, collection_name: str, document_id: str,
                        update_data: Dict[str, Union[int, str, dict]]) -> int:
        collection = self.db[collection_name]
        result = collection.update_one({'_id': ObjectId(document_id)}, {'$set': update_data})
        return result.modified_count

    def delete_document(self, collection_name: str, document_id: str) -> int:
        collection = self.db[collection_name]
        result = collection.delete_one({'_id': ObjectId(document_id)})
        return result.deleted_count
