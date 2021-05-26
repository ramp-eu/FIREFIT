from simple_pyueye import CameraObj

class Camera:
    def __init__(self):
        self.__camera = CameraObj(0)
        pass

    def connect(self):
        self.__camera.open()
        self.initialize()
        pass

    def disconnect(self):
        self.__camera.close()
        pass

    def initialize(self):
        pass

    def capture(self):
        img = self.__camera.capture_still() # options: save=True/false, if true: filename='file_path'
        # SERIALIZE _2d
        _2d_bytes = pickle.dumps(img)
        encoded = base64.b64encode(_2d_bytes)

        # MUST RETURN A JSON STRING AS:
        image = {
            "filename": "my_image{}".format(randrange(2000)),
            "image": encoded.decode('ascii')
        }
        return json.dumps(image)