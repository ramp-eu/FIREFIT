# Installation & Administration Guide

- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)

## Installation

To install and use this ROSE-AP, certain pre-requisites must be met. Although a `docker-compose` file is provided, enabling quick start-up of the system in an example scenario, the following middlewares must be provided in a custom application:

- A [MongoDB](https://www.mongodb.com/) instance (v3.6+) is required for data storage.
- A [Cygnus](https://fiware-cygnus.readthedocs.io/en/latest/https://fiware-cygnus.readthedocs.io/en/latest/) instance is used to interpret the [NGSI v2](https://fiware.github.io/specifications/ngsiv2/stable/) specification used by Orion and storing the context changes in each entity that is configured to be watched by Cygnus.
- A [JSON IoT Agent](https://fiware-iotagent-json.readthedocs.io/en/latest/) instance is needed to enable the integration of IoT devices with all its characteristics in the Orion Context Broker. Additionally, it behaves as a converter between distinct communication protocols that Orion does not understand to HTTP requests understandable by Orion.
- An MQTT broker to allow all the components to communicate via MQTT messages by using a publish/subscribe model. An example using [Eclipse Mosquitto](https://mosquitto.org/) is provided.


1. Clone the repository with the following command:

```bash
git clone https://github.com/Introsys/FIREFIT.ROSE-AP
```

2. Navigate to the path where the component repository was cloned.
3. Build the Docker image for the GCN:

```bash
cd src/gcn
docker build -t gcn .
```

4. Build the Docker image for the ICN:

```bash
cd src/icn
docker build -t icn .
```

## Usage

#### GitHub installation

In order to execute the ROSE-AP directly from the cloned repository, make sure the dependencies are met and issue the following commands:

1. Staring the GCN

```bash
cd src/gcn
python gcn.py
```

2. Starting the ICN

```bash
cd src/icn
./start.sh
```

#### Docker installation

Docker is the best way to use the ROSE-AP. After building the docker images for GCN and ICN respectively, a [`docker-compose`](../docker/docker-compose.yml) file can be used to ramp-up the stack and start all the needed services.

## Configuration

#### 1. GCN

There are three files that need to be configured in order to use GCN:

- [`configuration.json`](#11-configuration-file) - this Json file holds all the necessary parameters to configure GCN and how it connects to other services.
- [`camera.py`](#12-camera-file) - this Python file is responsible for holding all the necessary code to interact with the camera.
- [`Dockerfile`](#13-dockerfile) - this file is responsible for holding all the necessary elements to create a Docker image containing GCN.

Keep in mind the [current limitations of GCN](#14-current-limitations) through the configuration process.

The structure of each file will be presented in following sections.

##### 1.1. Configuration File

The `configuration.json` file is located at the `configuration` folder. Not only it defines how GCN will connect to other services but also how it is going to create the [Image Reference Entity](../src/gcn/data_models/image_reference.json) and the camera device.

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

##### 1.2. Camera File
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

##### 1.3. Dockerfile
Located at the `root` directory, the `Dockerfile` enables containerization of GCN, a common practice among other [Fiware services](https://www.fiware.org/developers/catalogue/).

```Dockerfile
FROM python:3.8-slim-buster

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

CMD ["python", "./cgn.py"]
```

##### 1.4. Current Limitations

GCN presents the following limitations at the current stage:

- only accepts `MQTT` as value for `iota_protocol`
- only accepts `mongo` as value for `sink`

#### 2. ICN

There are three files that need to be configured in order to use ICN:

- [`configuration.json`](#21-configuration-file) - this Json file holds all the necessary parameters to configure ICN and how it connects to other services.
- [`classifier.py`](#22-classifier-file) - this Python file is responsible for holding all the necessary code to perform the image classification tasks which may include data augmentation or preprocessing.
- [`Dockerfile`](#23-dockerfile) - this file is responsible for holding all the necessary elements to create a Docker image containing ICN.

Keep in mind the [current limitations of ICN](#24-current-limitations) through the configuration process.

The structure of each file will be presented in following sections.

##### 2.1. Configuration File

The `configuration.json` file is located at the `configuration` folder. Not only it defines how ICN will connect to other services but also how it is going to create the [Classification Result Entity](../src/icn/data_models/classification_result.json) and the classifier device. Additionally, it also specifies to which [Image Reference Entity](../src/gcn/data_models/image_reference.json) ICN will subscribe to. This file is located at the configuration folder.

An example of configuration is presented, where the endpoints make use of `hostname` instead of `ip address` for simplicity and convenience, since ICN is most likely to be used in a stack of docker containers.

```json
{
    "cb_endpoint": "http://orion:1026",
    "cygnus_endpoint": "http://cygnus:5051",
    "iota_endpoint": "http://iot-agent:4041",
    "iota_protocol": "MQTT",
    "protocol_broker_address": "mosquitto",
    "protocol_broker_port": "1883",
    "entity_id": "urn:ngsi-ld:ImageClassification:001",
    "image_entity_id": "urn:ngsi-ld:ImageRecord:001",
    "classifier_id": "urn:ngsi-ld:ImageClassifier:001",
    "api_key": "classifier",
    "service": "models",
    "service_path": "animals",
    "model_db_type": "mongo",
    "model_db_endpoint": "mongodb://mongo-db:27017",
    "host_ip": "icn",
    "host_port": "8181"
}
```

All parameters are mandatory, and a description of each is presented:

- `cb_endpoint` - the address (ip:port) of [Orion Context Broker](https://fiware-orion.readthedocs.io/en/master/)
- `cygnus_endpoint` - the address (ip:port) of [Cygnus](https://fiware-cygnus.readthedocs.io/en/latest/index.html), to which Orion will post HTTP messages to
- `iota_endpoint` - the address (ip:port) of [JSON IoT Agent](https://github.com/FIWARE/tutorials.IoT-Agent-JSON)
- `iota_protocol` - the transport parameter to be defined for the JSON IoT Agent, note that it must be [compliant with the acceptable parameters for the agent](https://github.com/FIWARE/tutorials.IoT-Agent-JSON) (`HTTP`, `MQTT` or `AMPQ`)
- `protocol_broker_address` - the address (ip) of the message broker for the protocol specified in `iota_protocol`
- `protocol_broker_port` - the port of the message broker for the protocol specified in `iota_protocol`
- `entity_id` - the id of the [Classification Result Entity](./data_models/classification_result.json) which will be created at Orion, [it is advised by Fiware](https://fiware-tutorials.readthedocs.io/en/latest/entity-relationships/index.html#creating-and-associating-data-entities) that it should respect the [NGSI-LD](https://www.etsi.org/deliver/etsi_gs/CIM/001_099/009/01.03.01_60/gs_cim009v010301p.pdf) specification
- `image_entity_id` - the id of the [Image Reference Entity](../GCN/data_models/image_reference.json) to whose changes ICN will subscribe to
- `classifier_id` - the id of the generic device that will be created as a classifier at JSON IoT Agent and, consequently, at Orion, following the same [advice provided by Fiware](https://fiware-tutorials.readthedocs.io/en/latest/entity-relationships/index.html#creating-and-associating-data-entities) regarding the [NGSI-LD](https://www.etsi.org/deliver/etsi_gs/CIM/001_099/009/01.03.01_60/gs_cim009v010301p.pdf) specification
- `api_key` - a [JSON IoT Agent](https://github.com/FIWARE/tutorials.IoT-Agent-JSON) specific configuration
- `service` - a [JSON IoT Agent](https://github.com/FIWARE/tutorials.IoT-Agent-JSON) specific configuration, it will also specify the database from where models will be consumed
- `service_path` - a [JSON IoT Agent](https://github.com/FIWARE/tutorials.IoT-Agent-JSON) specific configuration, it will also specify the database collection from where models will be consumed
- `model_db_type` - the type of database from where models will be consume
- `model_db_endpoint` - the model database endpoint
- `host_ip` - the address of the host machine which is running ICN, this is necessary so that Orion knows where to publish the [Image Reference Entity](../GCN/data_models/image_reference.json) context change notifications
- `host_port` - the port at which the host machine expect to receive the [Image Reference Entity](../GCN/data_models/image_reference.json) context change notifications, ICN will configure its API to the specified port

To understand the importance and role of the `api_key`, `service` and `service_path` parameters, one should be familiar with how [JSON IoT Agent operates](https://fiware-iotagent-json.readthedocs.io/en/latest/stepbystep/index.html).

##### 2.2. Classifier File

The `classifier.py` file, presents the necessary structure to allow users to implement the desired operations to perform image classification and it is located at the `icn_lib` Python module.

> ***It is imperative that the Python class structure is respected in order to ICN work properly.***

```python
class Classifier:
    def __init__(self):
        pass

    def initialization(self):
        pass

    def assign_model(self, db_file) -> object:
        return model_instance

    def preprocess(self, image) -> object:
        return preprocessed_image

    def classify(self, preprocessed_image, model) -> str:
        return 'classification_result'
```

Considering the rules applied by the [Python programming language](https://www.python.org/):

- `__init__` - class initialization
- `initialization` - executed after each `selectModel` classifier device command, allowing to setup whatever may be necessary after a new model instance is assigned as active
- `assign_model` - the model stored at the model database service and selected by the user through the `selectModel` classifier device command will be provided as an input for the `db_file` parameter. It is up to the user to transform the database content into a model instance using the same techniques considered for the model storing process.
- `preprocess` - the image stored at the image database service specified by the [Image Reference data model](../GCN/data_models/image_reference.json) is provided as an input for the `image` parameter. It is up to the user to transform the database content into an image format compatible with the classification process to be used. The techniques used for the image storing process should be considered here.
- `classify` - the outcome of the `preprocess` function is received as an input for the `preprocessed_image` parameter while the model instance returned by the `assign_model` function, and set as the currently active, is passed as an input for the `model` parameter. In this function, the image classification should be performed, being a `string` with the final outcome the expected result.

##### 2.3. Dockerfile

Located at the `root` directory, the `Dockerfile` enables containerization of ICN, a common practice among other [Fiware services](https://www.fiware.org/developers/catalogue/).

```dockerfile
FROM python:3.8-slim-buster

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

CMD ./start.sh
```

An example of configuration is presented in the [usage example section](#5-usage-example).

##### 2.4. Current Limitations

ICN presents the following limitations at the current stage:

- only accepts `MQTT` as value for `iota_protocol`
- only accepts `mongo` as value for `model_db_type`
- only accepts `mongo` as a `databaseType` parameter value of the [Image Reference data model](../src/gcn/data_models/image_reference.json) when receiving `classification` commands.
