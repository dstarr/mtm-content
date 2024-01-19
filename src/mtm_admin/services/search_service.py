import pymongo
import config


class SearchService:

    def __init__(self):
        pass

    def search_content(self, search_term):
        client = pymongo.MongoClient(config.COSMOS_DB_CONNECTION_STRING)
        db = client[config.COSMOS_DB_NAME]

        content_collection = None

        if db[config.COSMOS_DB_CONTENT_COLLECTION_NAME] is None:
            content_collection = db.create_collection(
                name=config.COSMOS_DB_CONTENT_COLLECTION_NAME)
        else:
            content_collection = db[config.COSMOS_DB_CONTENT_COLLECTION_NAME]

        query = {
            "$or": [
                {
                    "title": {
                        "$regex": search_term,
                        "$options": "i"
                    }
                },
                {
                    "description": {
                        "$regex": search_term,
                        "$options": "i"
                    }
                }
            ]
        }

        results = content_collection.find(query)

        return results.sort("title", pymongo.ASCENDING)
