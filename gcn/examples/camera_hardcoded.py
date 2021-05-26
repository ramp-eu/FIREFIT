import json
import pickle
import base64
from random import randrange
import numpy as np


class Camera:
    def __init__(self):
        self.connection_exceptions = ()
        pass

    def connect(self):
        try:
            print('CONNECT')
        except Exception as e:
            print(e)
        pass

    def disconnect(self):
        pass

    def initialize(self):
        try:
            print('INITIALIZE')
        except Exception as e:
            print(e)
        pass

    def capture(self) -> str:
        try:
            _2d = np.array([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                            [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]])

            # SERIALIZE _2d
            _2d_bytes = pickle.dumps(_2d)
            encoded = base64.b64encode(_2d_bytes)

            print('2d:', _2d)
            print('_2d_bytes:', _2d_bytes)
            print('encoded:', encoded)
            print('encoded.decode:', encoded.decode('ascii'))

            # MUST RETURN A JSON STRING AS:
            image = {
                "filename": "my_image{}".format(randrange(2000)),
                "image": encoded.decode('ascii')
            }

            # To consume
            #decoded = base64.b64decode(image['image'])
            #_2d_loaded = pickle.loads(decoded)

            #print('decoded:', decoded)
            #print('_2d_loaded:', _2d_loaded)

            return json.dumps(image)
        except Exception as e:
            print(e)
            return ''

    def configure(self, parameters):
        print('CONFIGURE:', parameters)
        pass
