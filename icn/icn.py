import getopt
import io
import sys

from icn_lib import logger
from icn_lib import Configuration
from icn_lib import Orion
from icn_lib import Iota
from icn_lib import ModelDB
from icn_lib import Classifier
from icn_lib import ClassifierEngine
from icn_lib import ProtoClient


def main(argv):
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
    logger.info('Configuring model database access.')

    model_db = ModelDB(config)
    model_db.configure_database_fs()

    logger.info('Successful.')
    logger.info('Add model.')

    opts, args = getopt.getopt(argv,"hf:",["ifile="])
    for opt, arg in opts:
        
        if opt in ("-f"):
            model = arg

        with io.FileIO(model, 'r') as f:
            model_db.put_model(model, f)
            logger.debug('Model saved to MongoDB')

    logger.info('Successful.')
    logger.info('Configuring image classifier.')

    classifier = Classifier()
    classifier_engine = ClassifierEngine(orion, classifier, model_db)

    logger.info('Successful.')
    logger.info('ICN is starting.')

    proto_client = ProtoClient(config, classifier_engine)
    proto_client.start()

if __name__ == "__main__":
    main(sys.argv[1:])
else:
    pass