# Installation & Administration Guide

- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)

## Installation

To install and use the GCN, certain pre-requisites must be met. Although a `docker-compose` file is provided, enabling quick start-up of the system in an example scenario, the following middlewares must be provided in a custom application:

- A [MongoDB](https://www.mongodb.com/) instance (v3.6+) is required for data storage.
- A [Cygnus](https://fiware-cygnus.readthedocs.io/en/latest/https://fiware-cygnus.readthedocs.io/en/latest/) instance is used to interpret the [NGSI v2](https://fiware.github.io/specifications/ngsiv2/stable/) specification used by Orion and storing the context changes in each entity that is configured to be watched by Cygnus.
- A [JSON IoT Agent](https://fiware-iotagent-json.readthedocs.io/en/latest/) instance is needed to enable the integration of IoT devices with all its characteristics in the Orion Context Broker. Additionally, it behaves as a converter between distinct communication protocols that Orion does not understand to HTTP requests understandable by Orion.
- An MQTT broker to allow all the components to communicate via MQTT messages by using a publish/subscribe model. An example using [Eclipse Mosquitto](https://mosquitto.org/) is provided.

Clone the repository with the following command:

```bash
git clone https://github.com/Introsys/FIREFIT.ROSE-AP
```

Navigate to the path where the component repository was cloned.

Build the Docker image for the GCN:

```bash
cd gcn
docker build -t gcn .
```

## Usage

### GitHub installation

In order to execute the GCN directly from the cloned repository, make sure the dependencies are met and issue the following command:

```bash
cd gcn
python gcn.py
```

### Docker installation

Docker is the best way to use the ROSE-AP. After building the docker image for GCN, a [`docker-compose`](../docker/docker-compose.yml) file can be used to ramp-up the stack and start all the needed services.

## Configuration

There are three files that need to be configured in order to use GCN:

- [`configuration.json`](#configuration-file) - this Json file holds all the necessary parameters to configure GCN and how it connects to other services.
- [`camera.py`](#camera-file) - this Python file is responsible for holding all the necessary code to interact with the camera.
- [`Dockerfile`](#dockerfile) - this file is responsible for holding all the necessary elements to create a Docker image containing GCN.

Keep in mind the [current limitations of GCN](#14-current-limitations) through the configuration process.

The structure of each file will be presented in following sections.

### Configuration File

The `configuration.json` file is located at the `configuration` folder. Not only it defines how GCN will connect to other services but also how it is going to create the [Image Reference Entity](../data_models/image_reference.json) and the camera device.

An example of configuration is presented, where the endpoints make use of `hostname` instead of `ip address` for simplicity and convenience, since GCN is most likely to be used in a stack of docker containers.

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
    "service_path": "ids",
    "sink": "mongo",
    "sink_endpoint": "mongodb://mongo-db:27017"
}
```

All parameters are mandatory, and a description of each is presented:

- `cb_endpoint` - the address (ip:port) of [Orion Context Broker](https://fiware-orion.readthedocs.io/en/master/)
- `cygnus_endpoint` - the address (ip:port) of [Cygnus](https://fiware-cygnus.readthedocs.io/en/latest/index.html), to which Orion will post HTTP messages to
- `iota_endpoint` - the address (ip:port) of [JSON IoT Agent](https://github.com/FIWARE/tutorials.IoT-Agent-JSON)
- `iota_protocol` - the transport parameter to be defined for the JSON IoT Agent, note that it must be [compliant with the acceptable parameters for the agent](https://github.com/FIWARE/tutorials.IoT-Agent-JSON) (`HTTP`, `MQTT` or `AMPQ`)
- `protocol_broker_address` - the address (ip) of the message broker for the protocol specified in `iota_protocol`
- `protocol_broker_port` - the port of the message broker for the protocol specified in `iota_protocol`
- `entity_id` - the id of the [Image Reference Entity](./data_models/image_reference.json) which will be created at Orion, [it is advised by Fiware](https://fiware-tutorials.readthedocs.io/en/latest/entity-relationships/index.html#creating-and-associating-data-entities) that it should respect the [NGSI-LD](https://www.etsi.org/deliver/etsi_gs/CIM/001_099/009/01.03.01_60/gs_cim009v010301p.pdf) specification
- `camera_id` - the id of the generic device that will be created as a camera at JSON IoT Agent and, consequently, at Orion, following the same [advice provided by Fiware](https://fiware-tutorials.readthedocs.io/en/latest/entity-relationships/index.html#creating-and-associating-data-entities) regarding the [NGSI-LD](https://www.etsi.org/deliver/etsi_gs/CIM/001_099/009/01.03.01_60/gs_cim009v010301p.pdf) specification
- `api_key` - a [JSON IoT Agent](https://github.com/FIWARE/tutorials.IoT-Agent-JSON) specific configuration
- `service` - a [JSON IoT Agent](https://github.com/FIWARE/tutorials.IoT-Agent-JSON) specific configuration, it will also specify the database to where images will be stored
- `service_path` - a [JSON IoT Agent](https://github.com/FIWARE/tutorials.IoT-Agent-JSON) specific configuration, it will also specify the database collection to where images will be stored
- `sink` - the type of sink to where images will be stored
- `sink_endpoint` - the sink address

To understand the importance and role of the `api_key`, `service` and `service_path` parameters, one should be familiar with how [JSON IoT Agent operates](https://fiware-iotagent-json.readthedocs.io/en/latest/stepbystep/index.html).

### Camera File

The `camera.py` file, presents the necessary structure to allow users to implement the desired operations to interact with the camera and it is located at the `GCNLib` Python module.

> ***It is imperative that the Python class structure is respected in order to GCN work properly.***

```python
import json

class Camera:
    def __init__(self):
        self.connection_exceptions = ()
        pass

    def connect(self):
        pass

    def disconnect(self):
        pass

    def initialize(self):
        pass

    def capture(self) -> str:
        # MUST RETURN A JSON STRING
        image = {
            "filename": "example_image",
            "image": "image_content"
        }
        return json.dumps(image)

    def configure(self, parameters):
        pass
```

Considering the rules applied by the [Python programming language](https://www.python.org/):

- `__init__` - class initialization, all the library specific `Exceptions` that will be defined in the `self.connection_exceptions` parameter `tuple` will trigger an automatic reconnect attempt, each time the camera disconnects raising one of the specified exceptions
- `connect` - necessary operations to connect to the camera
- `disconnects` - necessary operations to disconnect from the camera
- `initialize` - executed right after a successful `connect`, allows to perform initialization processes
- `capture` - necessary operations to capture an image, the return type must be a `JSON string` containing a `filename` and `image` keys, where the values are also of the type `string`. The return of this function will be sent to the specified `sink`
- `configure` - necessary operations to configure the camera, the `parameters` provided as a function input correspond to the specified value when issuing the device `configure` command

### Dockerfile

Located at the `root` directory, the `Dockerfile` enables containerization of GCN, a common practice among other [Fiware services](https://www.fiware.org/developers/catalogue/).

```Dockerfile
FROM python:3.8-slim-buster

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

CMD ["python", "./cgn.py"]
```

### Current Limitations

GCN presents the following limitations at the current stage:

- only accepts `MQTT` as value for `iota_protocol`
- only accepts `mongo` as value for `sink`
