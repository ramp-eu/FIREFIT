import time
import json
import threading
from . import logger


class CameraEngine:
    def __init__(self, orion, camera_module, database_service):
        self.is_busy = False
        self.__orion = orion
        self.__camera = camera_module
        self.__db = database_service
        self.__ths = []

    def connect(self):
        success = False
        try:
            self.__camera.connect()
            success = True
        except Exception as e:
            logger.error('Camera connect failed, exception: {}'.format(e))
        self.is_busy = False
        return success

    def disconnect(self):
        try:
            self.__camera.disconnect()
        except Exception as e:
            logger.error('Camera disconnect failed, exception: {}'.format(e))
        pass

    def initialize(self):
        try:
            self.__camera.initialize()
        except self.__camera.connection_exceptions as e:
            logger.error('Camera initialization failed, exception: {}'.format(e))
            self.recuperate()
        except Exception as e:
            logger.error('Camera initialization failed, exception: {}'.format(e))
        self.is_busy = False
        pass

    def capture(self):
        try:
            result = self.__camera.capture()
            result_dict = json.loads(result)
            filename = result_dict['filename']
            image = result_dict['image']

            # MULTITHREADED APPROACH DOES NOT GUARANTEE CB CONTEXT COHERENCY
            #t = threading.Thread(target=self.__store_image,
            #                     kwargs={'filename': filename, 'image': image})
            #self.__ths.append(t)
            #t.start()

            # Sync approach does.
            self.__store_image(filename, image)

        except self.__camera.connection_exceptions as e:
            logger.error('Camera capture failed, exception: {}'.format(e))
            self.recuperate()
        except Exception as e:
            logger.error('Camera capture failed, exception: {}'.format(e))
        self.is_busy = False
        pass

    def __store_image(self, filename, image):
        success = self.__db.put_image(filename, image)
        if success:
            self.__orion.update_image_entity(filename)
        pass

    def configure(self, parameters):
        try:
            self.__camera.configure(parameters)
        except self.__camera.connection_exceptions as e:
            logger.error('Camera configuration failed, exception: {}'.format(e))
            self.recuperate()
        except Exception as e:
            logger.error('Camera configuration failed, exception: {}'.format(e))
        self.is_busy = False
        pass

    def recuperate(self):
        for i in range(1, 6):
            time.sleep(5)
            logger.warning('Trying to reconnect to the camera... [{}]'.format(i))
            success = self.connect()
            if success:
                break
        logger.error('Could not reconnect to the camera.')


