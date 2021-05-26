

class Classifier:
    def __init__(self):
        pass

    def initialization(self):
        print('DEBUG INITIALIZATION')
        pass

    def assign_model(self, db_file) -> object:
        print('DEBUG ASSIGN MODEL')
        print(db_file)
        return 'model_instance'

    def preprocess(self, image) -> object:
        print('DEBUG PREPROCESS')
        print(image)
        return 'preprocessed_image'

    def classify(self, preprocessed_image, model) -> str:
        print('DEBUG CLASSIFY')
        print(preprocessed_image)
        print(model)
        return 'classification_result'
