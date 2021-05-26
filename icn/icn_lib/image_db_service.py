from . import logger
from .mongo_dao import MongoDAO


class ImageDB:
    def __init__(self, image_reference):
        self.__reference = image_reference
        self.__dao = self.__generate_dao(image_reference)

    def __generate_dao(self, image_reference):
        if image_reference['databaseType'] == 'mongo':
            return MongoDAO(image_reference['databaseEndpoint'])
        return None

    def configure_database_fs(self):
        success = False
        db_name = self.__reference['database']
        container_name = self.__reference['collection']
        if self.__dao.create_database(db_name):
            if self.__dao.create_fs(container_name):
                logger.debug('Database and container configured.')
                success = True
        if not success:
            logger.error('Error during database configuration.')
        return success

    def get_image(self):
        file = self.__dao.get(self.__reference['imageFile'])
        if file:
            logger.debug('File picked from database.')
        return file
