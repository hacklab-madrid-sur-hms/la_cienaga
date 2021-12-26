import pymongo
from itemadapter import ItemAdapter

class MongoPipeline(object):
    collection_name = 'contratos'

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(spider.config['mongo_connection'])
        self.db = self.client['la_cienaga']

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())

