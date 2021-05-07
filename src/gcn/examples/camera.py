import json

# for debug
import time
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

        # MUST RETURN A JSON STRING AS:
        image = {
            "filename": "my_image{}".format(randrange(2000)),
            "image": "image_content"
        }

        return json.dumps(image)

    def configure(self, parameters):
        print('DEBUG CONFIGURE', parameters)
        pass
