from . import logger
from .mongo_dao import MongoDAO


class ModelDB:
    def __init__(self, config):
        self.__configuration = config
        self.__dao = self.__generate_dao(config)

    def __generate_dao(self, config):
        if config.model_db_type == 'mongo':
            return MongoDAO(config.model_db_endpoint)
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

    def get_model(self, filename):
        file = self.__dao.get(filename)
        if file:
            logger.debug('File picked from database.')
        return file

    def exists_model(self, filename):
        return self.__dao.exists(filename)

    def put_model(self, filename, data):
        return self.__dao.put(filename, data)

    def list_models(self):
        return self.__dao.list_files()

