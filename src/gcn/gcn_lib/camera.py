import json
import pickle
import base64
import time
import numpy as np
from random import randrange


class Camera:
    def __init__(self):
        self.connection_exceptions = ()
        pass

    def connect(self):
        print('DEBUG CONNECT')
        pass

    def disconnect(self):
        print('DEBUG DISCONNECT')
        pass

    def initialize(self):
        print('DEBUG INITIALIZE')
        pass

    def capture(self) -> str:
        print('DEBUG CAPTURE')

        # SIMULATE CAPTURE TIME
        time.sleep(5)

        _2d = np.array([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])

        _2d_bytes = pickle.dumps(_2d)
        encoded = base64.b64encode(_2d_bytes)
        image_string = encoded.decode('ascii')

        # MUST RETURN A JSON STRING AS:
        image = {
            "filename": "my_image{}".format(randrange(2000)),
            "image": image_string
        }

        return_string = json.dumps(image)

        print('DEBUG RETURN STRING:', return_string)

        return return_string

    def configure(self, parameters):
        print('DEBUG CONFIGURE', parameters)
        pass