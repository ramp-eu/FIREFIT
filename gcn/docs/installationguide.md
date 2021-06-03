# Installation & Administration Guide

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Current Limitations](#current-limitations)

## Installation

To install and use the [GCN](../), certain pre-requisites must be met. Although a [`docker-compose`](../docker/docker-compose.yml) file is provided, enabling [quick start-up of the system in an example scenario](getting-started.md), the following middlewares must be provided in a custom application:

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

There are three files that need to be configured in order to use [GCN](../):

- [`configuration.json`](../configuration/configuration.json) - this [JSON](https://www.json.org) file holds all the necessary parameters to configure [GCN](../) and how it connects to other services.
- [`camera.py`](../gcn_lib/camera.py) - this [Python](https://www.python.org/) file is responsible for holding all the necessary code to interact with the camera.
- [`Dockerfile`](../Dockerfile) - this file is responsible for holding all the necessary elements to create a [Docker](https://docs.docker.com/) image containing [GCN](../).

Keep in mind the [current limitations of GCN](#current-limitations) through the configuration process.

### Configuration File

The [`configuration.json`](../configuration/configuration.json) file is located at the [`configuration`](../configuration) folder. Not only it defines how [GCN] will connect to other services but also how it is going to create the [Image Reference Entity](../data_models/image_reference.json) and the camera device.

An example of configuration is presented, where the endpoints make use of `hostname` instead of `ip address` for simplicity and convenience, since [GCN](../) is most likely to be used in a stack of docker containers.

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
- `cygnus_endpoint` - the address (ip:port) of [Cygnus](https://fiware-cygnus.readthedocs.io/en/latest/index.html), to which [Orion](https://fiware-orion.readthedocs.io/en/master/) will post HTTP messages to
- `iota_endpoint` - the address (ip:port) of [JSON IoT Agent](https://github.com/FIWARE/tutorials.IoT-Agent-JSON)
- `iota_protocol` - the transport parameter to be defined for the JSON IoT Agent, note that it must be [compliant with the acceptable parameters for the agent](https://github.com/FIWARE/tutorials.IoT-Agent-JSON) (`HTTP`, `MQTT` or `AMPQ`)
- `protocol_broker_address` - the address (ip) of the message broker for the protocol specified in `iota_protocol`
- `protocol_broker_port` - the port of the message broker for the protocol specified in `iota_protocol`
- `entity_id` - the id of the [Image Reference Entity](./data_models/image_reference.json) which will be created at [Orion](https://fiware-orion.readthedocs.io/en/master/), [it is advised by Fiware](https://fiware-tutorials.readthedocs.io/en/latest/entity-relationships/index.html#creating-and-associating-data-entities) that it should respect the [NGSI-LD](https://www.etsi.org/deliver/etsi_gs/CIM/001_099/009/01.03.01_60/gs_cim009v010301p.pdf) specification
- `camera_id` - the id of the generic device that will be created as a camera at JSON IoT Agent and, consequently, at [Orion](https://fiware-orion.readthedocs.io/en/master/), following the same [advice provided by Fiware](https://fiware-tutorials.readthedocs.io/en/latest/entity-relationships/index.html#creating-and-associating-data-entities) regarding the [NGSI-LD](https://www.etsi.org/deliver/etsi_gs/CIM/001_099/009/01.03.01_60/gs_cim009v010301p.pdf) specification
- `api_key` - a [JSON IoT Agent](https://github.com/FIWARE/tutorials.IoT-Agent-JSON) specific configuration
- `service` - a [JSON IoT Agent](https://github.com/FIWARE/tutorials.IoT-Agent-JSON) specific configuration, it will also specify the database to where images will be stored
- `service_path` - a [JSON IoT Agent](https://github.com/FIWARE/tutorials.IoT-Agent-JSON) specific configuration, it will also specify the database collection to where images will be stored
- `sink` - the type of sink to where images will be stored
- `sink_endpoint` - the sink address

To understand the importance and role of the `api_key`, `service` and `service_path` parameters, one should be familiar with how [JSON IoT Agent operates](https://fiware-iotagent-json.readthedocs.io/en/latest/stepbystep/index.html).

### Camera File

The [`camera.py`](../gcn_lib/camera.py) file presents the necessary structure to allow users to implement the desired operations to interact with the camera and it is located at the [`GCNLib`](../gcn_lib) Python module.

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

## Usage

To use the [GCN](../), navigate to the path where the repository was cloned and then to the component folder:

```bash
cd gcn
```

Execute the python application:

```bash
python gcn.py
```

>**Note:** ensure that the component is [configured](#configuration) and all [pre-requisites](#installation) are met.

### Docker

[Docker](https://www.docker.com/) is the best way to use the [GCN](../), as it is a common practice among other [FIWARE services](https://www.fiware.org/developers/catalogue/).

A pre-built image is located at [docker hub](https://hub.docker.com/repository/docker/introsyspt/gcn) for [quick testing](getting-started.md) the component. To get this image, issue the following command:

```bash
docker pull introsyspt/gcn:latest
```

In real-world applications though, the user is required to extend the [`camera.py`](../gcn_lib/camera.py) module and change the default [configuration](#configuration) to embrace its needs. After making all the [configurations](#configuration), one can use the [`Dockerfile`](../Dockerfile) located at the [`root`](../) directory to build a local image.

```Dockerfile
FROM python:3.8-slim-buster

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

CMD ["python", "./cgn.py"]
```

To build the image, use the command:

```bash
docker build -t gcn .
```

If the pre-requisites are met, that is, all required services are execution, one can execute the image directly:

- Using the docker hub image

```bash
docker run introsyspt/gcn
```

- Using the local image

```bash
docker run gcn
```

Additionally, a [`docker-compose`](../docker/docker-compose.yml) file can be used to ramp-up the stack and start all the needed services at once.

To execute, issue the following command:

```bash
cd docker
docker-compose -p gcn_stack up
```

To terminate:

```bash
docker-compose gcn_stack down
```

## Current Limitations

[GCN](../) presents the following limitations at the current stage:

- only accepts `MQTT` as value for `iota_protocol`
- only accepts `mongo` as value for `sink`

---

**Previous:** [Architecture](architecture.md) | **Next:** [Getting Started](getting-started.md)
