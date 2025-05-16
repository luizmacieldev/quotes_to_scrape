import hashlib
from pymongo import MongoClient, errors
from scrapy.exceptions import DropItem

class MongoDBPipeline:

    def open_spider(self, spider):
        self.client = MongoClient(spider.settings.get('MONGO_URI'))
        self.db = self.client[spider.settings.get('MONGO_DATABASE')]
        self.collection = self.db[spider.name]
        self.logger = spider.logger  # Usar o logger do Scrapy

    def close_spider(self, spider):
        self.client.close()

    def generate_unique_id(self, item):
        # Cria um hash MD5 do item para usar como _id
        item_str = str(item)  # Converte o item para string
        return hashlib.md5(item_str.encode('utf-8')).hexdigest()

    def process_item(self, item, spider):
        item['_id'] = self.generate_unique_id(item)
        try:
            self.collection.insert_one(dict(item))
        except errors.DuplicateKeyError:
            # Registra o item descartado e lança DropItem
            self.logger.warning(f"Item descartado: {item}")
            raise DropItem(f"Item duplicado encontrado: {item}")
        return item
