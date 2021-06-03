import shutil
import base64
import pickle
import numpy as np
import tensorflow as tf

class Classifier:
    def __init__(self):

        ### USER CODE:

        self.__class_names = ['daisy', 'dandelion', 'roses', 'sunflowers', 'tulips']

        ###

        pass

    def initialization(self):
        print('DEBUG INITIALIZATION')
        pass

    def assign_model(self, db_file) -> object:
        print('DEBUG ASSIGN MODEL')

        ### USER CODE:

        # reconstruct zip file from binary data
        with open('../flowers_model.zip', 'wb') as f:
            f.write(db_file)
        
        # extract zip file
        filename = '../flowers_model.zip'
        target_dir = '../flowers_model'
        archive_format = 'zip'
        shutil.unpack_archive(filename, target_dir, archive_format)

        # load model
        model = tf.keras.models.load_model('../flowers_model')

        ###

        print('DEBUG MODEL:', model)

        return model

    def preprocess(self, image) -> object:
        print('DEBUG PREPROCESS')

        # decode binary
        decoded_img_array = base64.b64decode(image)

        # convert to array
        img_array = pickle.loads(decoded_img_array)

        return img_array

    def classify(self, preprocessed_image, model) -> str:
        # predict
        predictions = model.predict(preprocessed_image)
        score = tf.nn.softmax(predictions[0])

        print(
            "This image most likely belongs to {} with a {:.2f} percent confidence.".format(
                self.__class_names[np.argmax(score)], 100 * np.max(score)
            )
        )

        # classify
        classification = self.__class_names[np.argmax(score)]

        return classification
