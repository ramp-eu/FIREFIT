from gcn_lib import logger
from gcn_lib import Configuration
from gcn_lib import Orion
from gcn_lib import Iota
from gcn_lib import DB
from gcn_lib import Camera
from gcn_lib import CameraEngine
from gcn_lib import MqttClient

if __name__ == '__main__':

    logger.info('Application starting.')

    config = Configuration()
    config.import_configuration('./configuration/')

    logger.info('Imported configuration:\n' + str(config))

    orion = Orion(config)

    logger.info('Orion purge process started.')

    orion.purge_subscriptions()

    logger.info('Configuring entities at Orion and data persistency at Cygnus.')

    orion.configure_entity()
    orion.configure_entity_data_pers()
    iota = Iota(config)
    iota.configure_device()

    logger.info('Successful.')
    logger.info('Configuring database access.')

    db = DB(config)
    db.configure_database_fs()

    logger.info('Successful.')
    logger.info('Importing user camera module.')

    camera = Camera()

    logger.info('Successful.')
    logger.info('Initializing the camera engine and connecting to the camera.')

    cam_eng = CameraEngine(orion, camera, db)

    cam_eng.connect()
    cam_eng.initialize()

    logger.info('Successful.')

    logger.info('Connecting to the MQTT and making device functions available.')

    cgn = MqttClient(config, cam_eng)
    cgn.start()
