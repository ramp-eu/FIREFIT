import json
import pickle
import base64
from random import randrange
from harvesters.core import Harvester


class Camera:
    def __init__(self):
        self.connection_exceptions = ()
        self.__harv = Harvester()
        self.__img_cap = None
        pass

    def connect(self):
        try:
            self.__harv.add_file('/usr/lib/ids/cti/ids_gevgentl.cti')
            self.__harv.update()
        except Exception as e:
            print(e)
        pass

    def disconnect(self):
        self.__img_cap.destroy()
        self.__harv.reset()
        pass

    def initialize(self):
        try:
            self.__img_cap = self.__harv.create_image_acquirer(list_index=0)
            self.__img_cap.remote_device.node_map.PixelFormat.value = 'Mono8'
        except Exception as e:
            print(e)
        pass

    def capture(self) -> str:
        try:
            # Start acquisition
            self.__img_cap.start_acquisition()

            with self.__img_cap.fetch_buffer() as buffer:
                component = buffer.payload.components[0]
                # reshape to a 2D array
                _2d = component.data.reshape(component.height, component.width)

            # Stop acquisition
            self.__img_cap.stop_acquisition()

            # SERIALIZE _2d
            _2d_bytes = pickle.dumps(_2d)
            encoded = base64.b64encode(_2d_bytes)

            print(_2d)
            print(_2d_bytes)
            print(encoded)

            # MUST RETURN A JSON STRING AS:
            image = {
                "filename": "my_image{}".format(randrange(2000)),
                "image": encoded.decode('ascii')
            }

            # To consume
            #decoded = base64.b64decode(image['image'])
            #_2d_loaded = pickle.loads(decoded)

            #print(decoded)
            #print(_2d_loaded)

            return json.dumps(image)
        except Exception as e:
            print(e)
            return None

    def configure(self, parameters):
        pass
