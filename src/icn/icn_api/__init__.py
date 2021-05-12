from .logger import logger
from .configuration import Configuration
from .schemas import ImageSubscriptionSchema
from .orion import Orion
from .protocol_client import ProtoClient

app_config = Configuration()
schema = ImageSubscriptionSchema()
orion = None

if __name__ == '__main__':
    pass
else:
    logger.info('API logging system initialized.')
    app_config.import_configuration('./configuration/')
    logger.info('Configuration imported.')
    orion = Orion(app_config)
    pass