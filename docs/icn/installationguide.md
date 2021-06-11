# Installation & Administration Guide

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Current Limitations](#current-limitations)

## Installation

To install and use the [ICN](https://github.com/Introsys/FIREFIT.ROSE-AP/tree/master/icn), certain pre-requisites must be met. Although a [`docker-compose`](../docker/docker-compose.yml) file is provided, enabling [quick start-up of the system in an example scenario](getting-started.md), the following middlewares must be provided in a custom application:

- A [MongoDB](https://www.mongodb.com/) instance (v3.6+) is required for data storage.
- An [Orion Context Broker](https://fiware-orion.readthedocs.io/en/master/) instance allows to manage information by making use of entities that can be seen as objects in the context of object oriented programming. It manages all the changes regarding those entities and allows the broadcast of those changes to all the other components that are connected to [Orion](https://fiware-orion.readthedocs.io/en/master/). There are a set of features that [Orion](https://fiware-orion.readthedocs.io/en/master/) makes available like the Publish/Subscribe or the registration of context providers to allow queries of information by demand.
- A [Cygnus](https://fiware-cygnus.readthedocs.io/en/latest/https://fiware-cygnus.readthedocs.io/en/latest/) instance is used to interpret the [NGSI v2](https://fiware.github.io/specifications/ngsiv2/stable/) specification used by Orion and storing the context changes in each entity that is configured to be watched by Cygnus.
- A [JSON IoT Agent](https://fiware-iotagent-json.readthedocs.io/en/latest/) instance is needed to enable the integration of IoT devices with all its characteristics in the [Orion Context Broker](https://fiware-orion.readthedocs.io/en/master/). Additionally, it behaves as a converter between distinct communication protocols that [Orion](https://fiware-orion.readthedocs.io/en/master/) does not understand to HTTP requests understandable by [Orion](https://fiware-orion.readthedocs.io/en/master/).
- An MQTT broker to allow all the components to communicate via MQTT messages by using a publish/subscribe model. An example using [Eclipse Mosquitto](https://mosquitto.org/) is provided.

After checking all the necessary dependencies, clone the repository using the following command:

```bash
git clone https://github.com/Introsys/FIREFIT.ROSE-AP
```

## Configuration

There are three files that need to be configured in order to use [ICN](https://github.com/Introsys/FIREFIT.ROSE-AP/tree/master/icn):

- [`configuration.json`](https://github.com/Introsys/FIREFIT.ROSE-AP/blob/master/icn/configuration/configuration.json) - this [JSON](https://www.json.org) file holds all the necessary parameters to configure [GCN](https://github.com/Introsys/FIREFIT.ROSE-AP/tree/master/gcn) and how it connects to other services.
- [`classifier.py`](https://github.com/Introsys/FIREFIT.ROSE-AP/blob/master/icn/icn_lib/classifier.py) - this [Python](https://www.python.org/) file is responsible for holding all the necessary code to perform the image classification tasks which may include data augmentation or preprocessing.
- [`Dockerfile`](https://github.com/Introsys/FIREFIT.ROSE-AP/blob/master/icn/Dockerfile) - this file is responsible for holding all the necessary elements to create a Docker image containing [ICN](https://github.com/Introsys/FIREFIT.ROSE-AP/tree/master/icn).

Keep in mind the [current limitations of ICN](#current-limitations) through the configuration process.

The structure of each file will be presented in following sections.

### Configuration File

The [`configuration.json`](https://github.com/Introsys/FIREFIT.ROSE-AP/blob/master/icn/configuration/configuration.json) file is located at the [`configuration`](https://github.com/Introsys/FIREFIT.ROSE-AP/tree/master/icn/configuration) folder. Not only it defines how [ICN](https://github.com/Introsys/FIREFIT.ROSE-AP/tree/master/icn) will connect to other services, but also how it is going to create the [Classification Result Entity](../data_models/classification_result.json) and the classifier device. Additionally, it also specifies to which [Image Reference Entity](https://github.com/Introsys/FIREFIT.ROSE-AP/blob/master/gcn/data_models/image_reference.json) [ICN](https://github.com/Introsys/FIREFIT.ROSE-AP/tree/master/icn) will subscribe to. This file is located at the [`configuration`](https://github.com/Introsys/FIREFIT.ROSE-AP/tree/master/icn/configuration) folder.

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
- `entity_id` - the id of the [Classification Result Entity](https://github.com/Introsys/FIREFIT.ROSE-AP/blob/master/icn/data_models/classification_result.json) which will be created at Orion, [it is advised by Fiware](https://fiware-tutorials.readthedocs.io/en/latest/entity-relationships/index.html#creating-and-associating-data-entities) that it should respect the [NGSI-LD](https://www.etsi.org/deliver/etsi_gs/CIM/001_099/009/01.03.01_60/gs_cim009v010301p.pdf) specification
- `image_entity_id` - the id of the [Image Reference Entity](https://github.com/Introsys/FIREFIT.ROSE-AP/blob/master/gcn/data_models/image_reference.json) to whose changes ICN will subscribe to
- `classifier_id` - the id of the generic device that will be created as a classifier at JSON IoT Agent and, consequently, at Orion, following the same [advice provided by Fiware](https://fiware-tutorials.readthedocs.io/en/latest/entity-relationships/index.html#creating-and-associating-data-entities) regarding the [NGSI-LD](https://www.etsi.org/deliver/etsi_gs/CIM/001_099/009/01.03.01_60/gs_cim009v010301p.pdf) specification
- `api_key` - a [JSON IoT Agent](https://github.com/FIWARE/tutorials.IoT-Agent-JSON) specific configuration
- `service` - a [JSON IoT Agent](https://github.com/FIWARE/tutorials.IoT-Agent-JSON) specific configuration, it will also specify the database from where models will be consumed
- `service_path` - a [JSON IoT Agent](https://github.com/FIWARE/tutorials.IoT-Agent-JSON) specific configuration, it will also specify the database collection from where models will be consumed
- `model_db_type` - the type of database from where models will be consume
- `model_db_endpoint` - the model database endpoint
- `host_ip` - the address of the host machine which is running ICN, this is necessary so that Orion knows where to publish the [Image Reference Entity](https://github.com/Introsys/FIREFIT.ROSE-AP/blob/master/gcn/data_models/image_reference.json) context change notifications
- `host_port` - the port at which the host machine expect to receive the [Image Reference Entity](https://github.com/Introsys/FIREFIT.ROSE-AP/blob/master/gcn/data_models/image_reference.json) context change notifications, [ICN](https://github.com/Introsys/FIREFIT.ROSE-AP/tree/master/icn) will configure its [API](api.md) to the specified port

To understand the importance and role of the `api_key`, `service` and `service_path` parameters, one should be familiar with how [JSON IoT Agent operates](https://fiware-iotagent-json.readthedocs.io/en/latest/stepbystep/index.html).

### Classifier File

The [`classifier.py`](https://github.com/Introsys/FIREFIT.ROSE-AP/blob/master/icn/icn_lib/classifier.py) file, presents the necessary structure to allow users to implement the desired operations to perform image classification and it is located at the [`icn_lib`](https://github.com/Introsys/FIREFIT.ROSE-AP/tree/master/icn/icn_lib) Python module.

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
- `preprocess` - the image stored at the image database service specified by the [Image Reference data model](https://github.com/Introsys/FIREFIT.ROSE-AP/blob/master/gcn/data_models/image_reference.json) is provided as an input for the `image` parameter. It is up to the user to transform the database content into an image format compatible with the classification process to be used. The techniques used for the image storing process should be considered here.
- `classify` - the outcome of the `preprocess` function is received as an input for the `preprocessed_image` parameter while the model instance returned by the `assign_model` function, and set as the currently active, is passed as an input for the `model` parameter. In this function, the image classification should be performed, being a `string` with the final outcome the expected result.

## Usage

To use the [ICN](https://github.com/Introsys/FIREFIT.ROSE-AP/tree/master/icn), navigate to the path where the repository was cloned and then to the component folder:

```bash
cd icn
```

Execute the python application:

```bash
start start.sh
```

>**Note:** ensure that the component is [configured](#configuration) and all [pre-requisites](#installation) are met.

### Docker

[Docker](https://www.docker.com/) is the best way to use the [ICN](https://github.com/Introsys/FIREFIT.ROSE-AP/tree/master/icn), as it is a common practice among other [FIWARE services](https://www.fiware.org/developers/catalogue/).

A pre-built image is located at [docker hub](https://hub.docker.com/repository/docker/introsyspt/icn) for [quick testing](getting-started.md) the component. To get this image, issue the following command:

```bash
docker pull introsyspt/icn:latest
```

In real-world applications though, the user is required to extend the [`classifier.py`](https://github.com/Introsys/FIREFIT.ROSE-AP/blob/master/icn/icn_lib/classifier.py) module and change the default [configuration](#configuration) to embrace its needs. After making all the [configurations](#configuration), one can use the [`Dockerfile`](https://github.com/Introsys/FIREFIT.ROSE-AP/blob/master/icn/Dockerfile) located at the [`root`](https://github.com/Introsys/FIREFIT.ROSE-AP/tree/master/icn) directory to build a local image.

```Dockerfile
FROM python:3.8-slim-buster

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

# user modules
#RUN pip install tensorflow

CMD ./start.sh
```

To build the image, use the command:

```bash
docker build -t icn .
```

If the pre-requisites are met, that is, all required services are execution, one can execute the image directly:

```bash
docker run introsyspt/icn
```

(if using the docker hub image)

```bash
docker run icn
```

(if using the local image)

Additionally, a [`docker-compose`](https://github.com/Introsys/FIREFIT.ROSE-AP/blob/master/icn/docker/docker-compose.yml) file can be used to ramp-up the stack and start all the needed services at once.

To execute, issue the following command:

```bash
cd docker
docker-compose -p icn_stack up
```

To terminate:

```bash
docker-compose icn_stack down
```

## Current Limitations

[ICN](https://github.com/Introsys/FIREFIT.ROSE-AP/tree/master/icn) presents the following limitations at the current stage:

- only accepts `MQTT` as value for `iota_protocol`
- only accepts `mongo` as value for `model_db_type`
- only accepts `mongo` as a `databaseType` parameter value of the [Image Reference data model](https://github.com/Introsys/FIREFIT.ROSE-AP/blob/master/gcn/data_models/image_reference.json) when receiving `classification` commands.

---

**Previous:** [Architecture](architecture.md) | **Next:** [Getting Started](getting-started.md)
