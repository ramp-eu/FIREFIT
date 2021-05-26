from . import logger
from . import ImageDB


class ClassifierEngine:
    def __init__(self, orion, classifier, model_db):
        self.is_busy = False
        self.__orion = orion
        self.__classifier = classifier
        self.__model_db = model_db
        self.active_model = None
        self.__active_model_name = ''

    def initialize(self):
        self.__classifier.initialization()

    def assign_model(self, model_name):
        validation = False
        if self.__model_db.exists_model(model_name):
            db_content = self.__model_db.get_model(model_name)
            self.active_model = self.__classifier.assign_model(db_content)
            self.__active_model_name = model_name
            self.__classifier.initialization()
            validation = True
        else:
            logger.warning('The model {} does not exist, assignment failed.'.format(model_name))
        self.is_busy = False
        return validation

    def classify(self, image_reference):
        validation = False
        if self.active_model is None:
            logger.warning('No model is active, set an active model before classifying.')
        else:
            try:
                image_db = ImageDB(image_reference)
                image_db.configure_database_fs()
                image = image_db.get_image()
                preprocessed_image = self.__classifier.preprocess(image)
                classification = self.__classifier.classify(preprocessed_image, self.active_model)
                self.__orion.update_classification_entity(image_reference,
                                                          self.__active_model_name,
                                                          classification)
                validation = True
            except Exception as e:
                logger.warning('Classification failed, exception: {}'.format(e))
        self.is_busy = False
        return validation

    def list_models(self):
        models = self.__model_db.list_models()
        self.is_busy = False
        return models




