from . import logger
from pymongo import MongoClient
import gridfs


class MongoDAO:
    def __init__(self, endpoint):
        self.__client = MongoClient(endpoint)
        self.__db = None
        self.__collection = None
        self.__fs = None

    def create_database(self, name):
        self.__db = self.__client[name]
        return True

    def get_database(self):
        return self.__db

    def create_collection(self, name):
        self.__collection = self.__db[name]
        return True

    def get_collection(self):
        return self.__collection

    def create_fs(self, name):
        self.__fs = gridfs.GridFS(database=self.__db, collection=name)
        return True

    def put(self, filename, data):
        try:
            f = self.__fs.find_one({'filename': filename})
            if not f:
                self.__fs.put(data, encoding='utf-8', filename=filename)
                return True
            else:
                logger.warning("A file with name '{}' already exists, image not saved.".format(filename))
                return False
        except Exception as e:
            logger.error('Error when sending data to MongoDB: {}'.format(e))
            return False

    def get(self, filename):
        file = self.__fs.find_one({'filename': filename})
        content = file.read()
        return content

    def list_databases(self):
        return self.__client.list_database_names()




