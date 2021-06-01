import PIL
import json
import pickle
import base64
import tensorflow as tf
from random import randrange
from tensorflow import keras

class Camera:
    def __init__(self):
        self.connection_exceptions = ()
        self.__img_height = 180
        self.__img_width = 180
        self.__sunflower_url = "https://storage.googleapis.com/download.tensorflow.org/example_images/592px-Red_sunflower.jpg"
        self.__sunflower_path = None
        pass

    def connect(self):
        print('DEBUG CONNECT')
        pass

    def disconnect(self):
        print('DEBUG DISCONNECT')
        pass

    def initialize(self):
        print('DEBUG INITIALIZE')
        self.__sunflower_path = tf.keras.utils.get_file('Red_sunflower', origin=self.__sunflower_url)
        pass

    def capture(self) -> str:
        print('DEBUG CAPTURE')

        img = keras.preprocessing.image.load_img(
            self.__sunflower_path, target_size=(self.__img_height, self.__img_width)
        )
        img_array = keras.preprocessing.image.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0)  # Create a batch

        # Encode image
        array_bytes = pickle.dumps(img_array)
        encoded = base64.b64encode(array_bytes)
        array_string = encoded.decode('ascii')

        # Necessary structure to store
        image = {
            "filename": "red_sunflower_{}".format(randrange(2000)),
            "image": array_string
        }

        return_string = json.dumps(image)

        print('DEBUG RETURN STRING:', return_string)

        return return_string

    def configure(self, parameters):
        print('DEBUG CONFIGURE', parameters)
        pass