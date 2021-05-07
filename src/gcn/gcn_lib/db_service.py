from . import logger
from .mongo_dao import MongoDAO


class DB:
    def __init__(self, config):
        self.__configuration = config
        self.__dao = self.__generate_dao(config)

    def __generate_dao(self, config):
        if config.sink == 'mongo':
            return MongoDAO(config.sink_endpoint)
        return None

    def configure_database_fs(self):
        success = False
        db_name = self.__configuration.service
        container_name = self.__configuration.service_path
        if self.__dao.create_database(db_name):
            if self.__dao.create_fs(container_name):
                logger.debug('Database and container configured.')
                success = True
        if not success:
            logger.error('Error during database configuration.')
        return success

    def put_image(self, filename, image):
        success = False
        if self.__dao.put(filename, image):
            success = True
            logger.debug('Image sent to database.')
        return success

    def get_image(self, filename):
        image = self.__dao.get(filename)
        if image:
            logger.debug('Image picked from database.')
        return image

