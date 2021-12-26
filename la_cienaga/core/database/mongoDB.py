from la_cienaga.core.abc.db import DB
import pymongo

class MongoDB(DB):
    def connect(self, db):
        self._client = pymongo.MongoClient(self._mongo_connection)
        self._db = self._client[db]

    def close(self):
        pass
