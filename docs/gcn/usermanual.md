# User Manual

This section provides information to configure and build application specific versions of the [GCN](https://github.com/Introsys/FIREFIT.ROSE-AP/tree/master/gcn).

## Configuration

Starting with the [`configuration.json`](https://github.com/Introsys/FIREFIT.ROSE-AP/blob/master/gcn/configuration/configuration.json):

```json
{
    "cb_endpoint": "http://orion:1026",
    "cygnus_endpoint": "http://cygnus:5051",
    "iota_endpoint": "http://iot-agent:4041",
    "iota_protocol": "MQTT",
    "protocol_broker_address": "mosquitto",
    "protocol_broker_port": "1883",
    "entity_id": "urn:ngsi-ld:ImageRecord:001",
    "camera_id": "urn:ngsi-ld:Camera:001",
    "api_key": "camera",
    "service": "production",
    "service_path": "manufacturer",
    "sink": "mongo",
    "sink_endpoint": "mongodb://mongo-db:27017"
}
```

By comparing with the [`docker-compose`](https://github.com/Introsys/FIREFIT.ROSE-AP/blob/master/gcn/docker/docker-compose.yml), it is possible to quickly correlate the defined parameters with the `hostname` and exposed/configured ports of each service. The id `urn:ngsi-ld:ImageRecord:001` will be assigned to the [Image Reference Entity](https://github.com/Introsys/FIREFIT.ROSE-AP/blob/master/gcn/data_models/image_reference.json) that will be created at [Orion](https://fiware-orion.readthedocs.io/en/master/). The id `urn:ngsi-ld:Camera:001` will be assigned to the camera device that will be created at [Orion](https://fiware-orion.readthedocs.io/en/master/) through [JSON IoT Agent](https://fiware-iotagent-json.readthedocs.io/en/latest/stepbystep/index.html). Each image will be stored at the `manufacturer` collection of the `production` database from a MongoDB instance (`mongo` defined as `sink`).

As for the [`camera.py`](https://github.com/Introsys/FIREFIT.ROSE-AP/blob/master/gcn/gcn_lib/camera.py):

```python
import json
import time
from random import randrange

class Camera:
    def __init__(self):
        self.connection_exceptions = (ConnectionError)
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

        # Simulate capture time
        time.sleep(5)
        
        # Create an image as a Numpy array
        image = np.array([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])

        # Serialize to bytes
        image_bytes = pickle.dumps(image)

        # Encode to base64
        image_encoded = base64.b64encode(image_bytes)

        # Convert to string
        image_string = image_encoded.decode('ascii')

        # Build the necessary json structure
        image_file = {
            "filename": "my_image{}".format(randrange(2000)),
            "image": image_string
        }

        # Convert to json string
        return_string = json.dumps(image_file)

        print('DEBUG RETURN STRING:', return_string)

        return return_string

    def configure(self, parameters):
        print('DEBUG CONFIGURE:', parameters)
        pass
```

The `ConnectionError` is the `Exception` defined as the one which will trigger reconnection attempts. In this example, simple `print` commands will be issued to allow visual feedback of each function trigger.

For the `capture` function, a [NumPy](https://numpy.org/) array is created in attempt to simulate a typical image data structure. One can interpret this array as a 10x10 grayscale image, being 0 the color black and 1 the color white, any value in between is a gray tone. Since the image needs to be included in a json structure, it will be encoded into a string, being the result of the encoding conveniently subject to a `print` before the `return` statement.

The `configure` function will directly `print` the parameters sent with the `configure` device command.

It is important to note that the contents of these functions depend on each user goals and eventually on each camera manufacturer. A user may not need to perform initialization tasks while another may wish to set several manufacturer specific camera parameters. A user may want to store images as [NumPy](https://numpy.org/) arrays while other may wish to store as an encoded `jpeg`. It all comes down to each user's needs.

## Dockerization


Finally, it is time to prepare the containerization of GCN using the [`Dockerfile`](https://github.com/Introsys/FIREFIT.ROSE-AP/blob/master/gcn/Dockerfile):

```Dockerfile
FROM python:3.8-slim-buster

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

# user modules
RUN pip install numpy

CMD ["python", "./cgn.py"]
```

Since [NumPy](https://numpy.org/) is not a built-in Python package and it is used in this example, it needs to be installed. For that reason, an additional `RUN` command is issued to perform the operation. The Docker image is then [created]((https://docs.docker.com/engine/reference/commandline/build/)) with the name `gcn`:

> ***The docker image name must correspond to the one defined at the docker-compose.yml file presented at the beginning of the example.***

```console
docker build -t gcn .
```

Finally, it is time to prepare the containerization of GCN using the [`Dockerfile`](https://github.com/Introsys/FIREFIT.ROSE-AP/blob/master/gcn/Dockerfile):

```Dockerfile
FROM python:3.8-slim-buster

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

# user modules
RUN pip install numpy

CMD ["python", "./cgn.py"]
```

Since [NumPy](https://numpy.org/) is not a built-in Python package and it is used in this example, it needs to be installed. For that reason, an additional `RUN` command is issued to perform the operation. The Docker image is then [created]((https://docs.docker.com/engine/reference/commandline/build/)) with the name `gcn`:

> ***The docker image name must correspond to the one defined at the docker-compose.yml file presented at the beginning of the example.***

```console
docker build -t gcn .
```

---

**Previous:** [Getting Started](getting-started.md)
