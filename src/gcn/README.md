# GCN - Generic Camera Node
# 1. Introduction
The Generic Camera Node (GCN) is a component that aims to easily integrate any generic camera into a Fiware solution, abstracting the user from entity, device, database and data persistency configurations.


GCN provides the image capture and camera configuration functionalities, and also ensures the obtained images data persistency to a user-defined database service.

>***Note that at the current state only MongoDB is considered, but the component was designed to scale to other types of database services in the future.***

To achieve this, the user is required to develop the necessary mechanisms using the [Python](https://www.python.org/) programming language. All the necessary structures are provided so that the user only has to *fill the gaps*. All the necessary steps to do so are described in the [configuration section](#4-configuration).

# 2. Dependencies

To ensure proper functionality, GCN depends on the following services:

- Fiware
  - Orion Context Broker
  - JSON IoT Agent
  - Cygnus
- Third-party
  - MongoDB
  - Mosquitto

These services are presented with detail in the [FIREFIT Rose-AP repository documentation](../README.md).

# 3. Operation Principle

> **In short terms, GCN will make a configurable camera device available at Orion that allows users to capture images while storing them in a database service.**

When GCN starts it communicates via HTTP with Orion, creating the [Image Reference Entity](./data_models/image_reference.json) and the corresponding data persistency, ensured by Cygnus. Then, it communicates with JSON IoT Agent also via HTTP to create the camera device, which in turn will create the corresponding entity at Orion (IoT Agent intrinsic functionality). From this point on, a camera device with the `capture` and `configure` commands is available at Orion, and the intrinsic functionality of generic devices is ensured by the JSON IoT Agent.

At each `capture` command issued, the GCN will perform the user-defined capture operation and will store the corresponding result at the image database service, updating the [Image Reference Entity](./data_models/image_reference.json) with the corresponding context data at Orion.

At each `configure` command issued, the GCN will perform the user-defined camera configuration operation, updating the device attributes at Orion to reflect the current configuration.

To issue these commands one can use HTTP requests or direct MQTT messages, both respecting the [Fiware JSON IoT Agent](https://fiware-iotagent-json.readthedocs.io/en/latest/) functionality. For the latter, one needs to be aware that the IoT Agent will not be handling the execution requests ([southbound functionality](https://fiware-tutorials.readthedocs.io/en/latest/iot-agent/index.html)) and therefore will not update the device context data to `PENDING` status for the corresponding command.

The following image presents how GCN positions itself in a Fiware solution:

<div>
  <p align="center">
    <img src="../../docs/gcn.png"/>
  </p>
  <p align="center">Generic Camera Node</p>
</div>

Note that the dependency on a message broker such as Mosquitto (depending on IoT Agent configuration) and on the entity data persistency service Cygnus still exist. In the previous image, these can be considered to be implicitly included into the IoT Agent and Orion respectively.


# 4. Configuration
There are three files that need to be configured in order to use GCN:

- [`configuration.json`](#41-configuration-json) - this Json file holds all the necessary parameters to configure GCN and how it connects to other services.
- [`camera.py`](#42-camera-py) - this Python file is responsible for holding all the necessary code to interact with the camera.
- [`Dockerfile`](#43-dockerfile) - this file is responsible for holding all the necessary elements to create a Docker image containing GCN.

Keep in mind the [current limitations of GCN](#44-current-limitations) through the configuration process.

The structure of each file will be presented in following sections.

## 4.1. Configuration File
The `configuration.json` file is located at the `configuration` folder. Not only it defines how GCN will connect to other services but also how it is going to create the [Image Reference Entity](./data_models/image_reference.json) and the camera device.

An example of configuration is presented, where the endpoints make use of `hostname` instead of `ip address` for simplicity and conveniency, since GCN is most likely to be used in a stack of docker containers. 

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

An example of configuration is presented in the [usage example section](#5-usage-example).

## 4.2. Camera File
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

An example of configuration is presented in the [usage example section](#5-usage-example).

## 4.3. Dockerfile
Located at the `root` directory, the `Dockerfile` enables containerization of GCN, a common practice among other [Fiware services](https://www.fiware.org/developers/catalogue/).

```Dockerfile
FROM python:3.8-slim-buster

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

CMD ["python", "./cgn.py"]
```
An example of configuration is presented in the [usage example section](#5-usage-example).

## 4.4. Current Limitations
GCN presents the following limitations at the current stage:
- only accepts `MQTT` as value for `iota_protocol`
- only accepts `mongo` as value for `sink`

# 5. Usage Example
In this section, a GCN configuration and usage example is presented.

> ***Be aware that the following content should be used as a reference only and not as a production ready solution. There are several security concerns that should be taken into account depending on the context where CGN will operate.***

In order to produce the same results as presented here, it is advised to use the [Visual Studio Code](https://code.visualstudio.com/) [REST Client extension](https://github.com/Huachao/vscode-restclient) to perform HTTP requests, it is also available at the Extensions menu.

As a starting point, although the GCN image is not yet created, it is important to define and understand which services are necessary to ensure the GCN functionality, as mentioned in the [dependencies section](#2-dependencies). For this reason, the following `docker-compose.yaml` file represents the deployment of the present example:

```yaml
version: "3.5"
services:
  # Orion is the context broker
  orion:
    image: fiware/orion:2.4.0
    hostname: orion
    container_name: fiware-orion
    depends_on:
      - mongo-db
    networks:
      - default
    ports:
      - "1026:1026"
    command: -dbhost mongo-db -logLevel DEBUG -noCache -insecureNotif

  # Databases
  mongo-db:
    image: mongo:3.6
    hostname: mongo-db
    container_name: db-mongo
    expose:
      - "27017"
    ports:
      - "27017:27017"
    networks:
      - default
    command: --bind_ip_all --smallfiles
  
  # IoT Agent (JSON)
  iot-agent:
    image: fiware/iotagent-json:latest
    hostname: iot-agent
    container_name: fiware-iot-agent
    depends_on:
        - mongo-db
    networks:
        - default
    expose:
        - "4041"
    ports:
        - "4041:4041"
    environment:
        - IOTA_CB_HOST=orion
        - IOTA_CB_PORT=1026
        - IOTA_NORTH_PORT=4041
        - IOTA_REGISTRY_TYPE=mongodb
        - IOTA_LOG_LEVEL=DEBUG
        - IOTA_TIMESTAMP=true
        - IOTA_CB_NGSI_VERSION=v2
        - IOTA_AUTOCAST=true
        - IOTA_MONGO_HOST=mongo-db
        - IOTA_MONGO_PORT=27017
        - IOTA_MONGO_DB=iotagentjson
        - IOTA_PROVIDER_URL=http://iot-agent:4041
        - IOTA_DEFAULT_RESOURCE=/iot/json
        - IOTA_MQTT_HOST=mosquitto
        - IOTA_MQTT_PORT=1883

  # MQTT broker
  mosquitto:
    image: eclipse-mosquitto
    hostname: mosquitto
    container_name: mosquitto
    networks:
        - default
    expose:
        - "1883"
    ports:
        - "1883:1883"
  
  # Data Persistence
  cygnus:
    image: fiware/cygnus-ngsi:latest
    hostname: cygnus
    container_name: fiware-cygnus
    depends_on:
        - mongo-db
    networks:
        - default
    environment:
        - "CYGNUS_MONGO_HOSTS=mongo-db:27017"
        - "CYGNUS_MONGO_SERVICE_PORT=5051"
        - "CYGNUS_LOG_LEVEL=DEBUG"
        - "CYGNUS_API_PORT=5080"
        - "CYGNUS_SERVICE_PORT=5051"

  # GCN
  gcn:
    image: gcn
    hostname: gcn
    container_name: gcn
    depends_on:
        - orion
        - iot-agent
        - mosquitto
        - mongo-db
    networks:
        - default

networks:
  default:
    ipam:
      config:
        - subnet: 172.18.1.0/24

volumes:
  mongo-db: ~

```

The relevant elements to consider regarding the `docker-compose` are:
- The usage of `MQTT` protocol and therefore the `mosquitto` broker
- `hostname` of each service
- `expose` specified ports, stating that those ports will be exposed within the **docker network**
- `ports` specified ports, stating that those ports will be exposed to the **host machine**

A description of the complete addresses (address:port) for each service, given the presented `docker-compose` is as follows:
- Orion - `orion:1026`
- MongoDB - `mongo-db:27017`
- JSON IoT Agent - `iot-agent:4041`
- Mosquitto (MQTT broker) - `mosquitto:1883`
- Cygnus - `cygnus:5051`

Having a deployment that ensures the minimal service requirements for GCN, the next step is to configure the necessary files before building the GCN image.

Starting with the `configuration.json`:

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

By comparing with the `docker-compose`, it is possible to quickly correlate the defined parameters with the `hostname` and exposed/configured ports of each service. The id `urn:ngsi-ld:ImageRecord:001` will be assigned to the [Image Reference Entity](./data_models/image_reference.json) that will be created at Orion. The id `urn:ngsi-ld:Camera:001` will be assigned to the camera device that will be created at Orion through JSON IoT Agent. Each image will be stored at the `manufacturer` collection of the `production` database from a MongoDB instance (`mongo` defined as `sink`).

As for the `camera.py`:

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

Finally, it is time to prepare the containerization of GCN using the `Dockerfile`:

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

The only remaining step to deploy GCN is to use the `docker-compose.yaml` file to create all the service instances:

```console
docker-compose -p gcn_stack up -d
```

By running the docker command to check the running containers:

```console
docker container ls --all
```

One should obtain the following result:

```console
CONTAINER ID   IMAGE                         COMMAND                  CREATED          STATUS          PORTS                              NAMES
50d8262d9537   gcn                           "python ./cgn.py"        11 minutes ago   Up 11 minutes                                      gcn
8b7467ef977a   fiware/cygnus-ngsi:latest     "/cygnus-entrypoint.…"   11 minutes ago   Up 11 minutes   5050/tcp, 5080/tcp                 fiware-cygnus
0212052b2e2e   fiware/orion:2.4.0            "/usr/bin/contextBro…"   11 minutes ago   Up 11 minutes   0.0.0.0:1026->1026/tcp             fiware-orion
72bbe96da225   fiware/iotagent-json:latest   "docker/entrypoint.s…"   11 minutes ago   Up 11 minutes   0.0.0.0:4041->4041/tcp, 7896/tcp   fiware-iot-agent
3aa2f8d41d86   eclipse-mosquitto             "/docker-entrypoint.…"   11 minutes ago   Up 11 minutes   0.0.0.0:1883->1883/tcp             mosquitto
3b2cc0820f9d   mongo:3.6                     "docker-entrypoint.s…"   11 minutes ago   Up 11 minutes   0.0.0.0:27017->27017/tcp           db-mongo
```

Using [Visual Studio Code](https://code.visualstudio.com/) with the [REST Client extension](https://github.com/Huachao/vscode-restclient), it is possible to query Orion for its entities:

```http
### Get Orion Entities
GET http://localhost:1026/v2/entities
```

Which should respond with the following result:

```http
HTTP/1.1 200 OK
Connection: close
Content-Length: 252
Content-Type: application/json
Fiware-Correlator: e55bc724-9217-11eb-a082-0242ac120106
Date: Wed, 31 Mar 2021 11:54:49 GMT

[
  {
    "id": "urn:ngsi-ld:ImageRecord:001",
    "type": "imageReference",
    "image": {
      "type": "reference",
      "value": {
        "databaseType": "mongo",
        "databaseEndpoint": "mongodb://mongo-db:27017",
        "database": "production",
        "collection": "/manufacturer",
        "imageFile": ""
      },
      "metadata": {}
    }
  }
]
```

The only existing entity is the [Image Reference Entity](./data_models/image_reference.json), confirming that it was successfully configured as a context entity with the configured id `urn:ngsi-ld:ImageRecord:001`. The successful creation of the camera device entity is yet to be confirmed, and to do so, the `service` and `service-path` need to be considered when querying Orion:

```http
### Device entities at production service and manufacturer service-path
GET http://localhost:1026/v2/entities
fiware-service: production
fiware-servicepath: /manufacturer
```

The response should be as follows:

```http
HTTP/1.1 200 OK
Connection: close
Content-Length: 585
Content-Type: application/json
Fiware-Correlator: c4e821e4-9218-11eb-ac1f-0242ac120106
Date: Wed, 31 Mar 2021 12:01:04 GMT

[
  {
    "id": "urn:ngsi-ld:Camera:001",
    "type": "camera",
    "TimeInstant": {
      "type": "DateTime",
      "value": "2021-03-31T11:33:27.00Z",
      "metadata": {}
    },
    "capture_info": {
      "type": "commandResult",
      "value": " ",
      "metadata": {}
    },
    "capture_status": {
      "type": "commandStatus",
      "value": "UNKNOWN",
      "metadata": {}
    },
    "configuration": {
      "type": "String",
      "value": " ",
      "metadata": {}
    },
    "configure_info": {
      "type": "commandResult",
      "value": " ",
      "metadata": {}
    },
    "configure_status": {
      "type": "commandStatus",
      "value": "UNKNOWN",
      "metadata": {}
    },
    "capture": {
      "type": "command",
      "value": "",
      "metadata": {}
    },
    "configure": {
      "type": "command",
      "value": "",
      "metadata": {}
    }
  }
]
```

One can infer that the device configuration was successfully performed, having the camera device available with the `capture` and `configure` commands as well as the `configuration` attribute stating the current configuration of the device. The configured id `urn:ngsi-ld:Camera:001` is also confirmed. Since the device was created at Orion through an intrinsic mechanism of JSON IoT Agent, it is possible to query the Agent to validate that the same representation of the device is defined, note the distinct address to where the HTTP request is sent:

```http
### Devices defined at production service and manufacturer service-path
GET http://localhost:4041/iot/devices
fiware-service: production
fiware-servicepath: /manufacturer
```

The response should be as follows:

```http
HTTP/1.1 200 OK
X-Powered-By: Express
Fiware-Correlator: 5b32aa08-2d6a-4633-a933-a268f4049961
Content-Type: application/json; charset=utf-8
Content-Length: 487
ETag: W/"1e7-ScOS7YGWMXdbFhl5djuwpNdwLWY"
Date: Wed, 31 Mar 2021 12:04:31 GMT
Connection: close

{
  "count": 1,
  "devices": [
    {
      "device_id": "urn:ngsi-ld:Camera:001",
      "service": "production",
      "service_path": "/manufacturer",
      "entity_name": "urn:ngsi-ld:Camera:001",
      "entity_type": "camera",
      "transport": "MQTT",
      "attributes": [
        {
          "object_id": "configuration",
          "name": "configuration",
          "type": "String"
        }
      ],
      "lazy": [],
      "commands": [
        {
          "object_id": "capture",
          "name": "capture",
          "type": "command"
        },
        {
          "object_id": "configure",
          "name": "configure",
          "type": "command"
        }
      ],
      "static_attributes": [],
      "protocol": "json",
      "explicitAttrs": false
    }
  ]
}
```

The same device structure is presented, an expected result since it is the JSON IoT Agent the one responsible for creating the device entity at Orion.

Another important query to JSON IoT Agent will determine if the proper `api_key` was defined, it is an important element since it will define part of the `MQTT` topics to which the IoT Agent will publish and subscribe to:

```http
### Check IoT Agent Services for the production service and any (*) service-path
GET http://localhost:4041/iot/services
fiware-service: production
fiware-servicepath: /*
```

The response should be as follows:

```http
HTTP/1.1 200 OK
X-Powered-By: Express
Fiware-Correlator: 3fb3351f-7769-4d5b-bc2e-08a20d3202c9
Content-Type: application/json; charset=utf-8
Content-Length: 271
ETag: W/"10f-WvT/c0WpK9Azpgd+fU1Ru1tyw7c"
Date: Wed, 31 Mar 2021 13:07:47 GMT
Connection: close

{
  "count": 1,
  "services": [
    {
      "commands": [],
      "lazy": [],
      "attributes": [],
      "_id": "60645e06eee1540007a709c9",
      "resource": "/iot/json",
      "apikey": "camera",
      "service": "production",
      "subservice": "/manufacturer",
      "__v": 0,
      "static_attributes": [],
      "internal_attributes": [],
      "entity_type": "camera"
    }
  ]
}
```

One can infer that the `api_key`, `service` and `service-path` defined at the `configuration.json` are properly defined as a service, a mechanism used by [JSON IoT Agent](https://fiware-iotagent-json.readthedocs.io/en/latest/stepbystep/index.html).

The only remaining element that is yet to be confirmed regarding Orion is the [Image Reference Entity](./data_models/image_reference.json) data persistency. To do so, a query to Orion's subscriptions will be performed:

```http
### Orion subscriptions
GET http://localhost:1026/v2/subscriptions
```

Yielding the response:

```http
HTTP/1.1 200 OK
Connection: close
Content-Length: 478
Content-Type: application/json
Fiware-Correlator: 8779bfd8-9223-11eb-8be7-0242ac120106
Date: Wed, 31 Mar 2021 13:18:05 GMT

[
  {
    "id": "60645e06f866675751fc2409",
    "description": "Image Reference data persistence subscription.",
    "status": "active",
    "subject": {
      "entities": [
        {
          "id": "urn:ngsi-ld:ImageRecord:001",
          "type": "imageReference"
        }
      ],
      "condition": {
        "attrs": [
          "image"
        ]
      }
    },
    "notification": {
      "timesSent": 1,
      "lastNotification": "2021-03-31T11:33:26.00Z",
      "attrs": [],
      "onlyChangedAttrs": false,
      "attrsFormat": "normalized",
      "http": {
        "url": "http://cygnus:5051/notify"
      },
      "lastSuccess": "2021-03-31T11:33:26.00Z",
      "lastSuccessCode": 200
    }
  }
]
```

This confirms that Orion is notifying the Cygnus service regarding changes to the [Image Reference Entity](./data_models/image_reference.json). Fiware provides a detailed [step-by-step guide](https://fiware-tutorials.readthedocs.io/en/latest/historic-context-flume/index.html#mongodb-reading-data-from-a-database) on how to confirm that data is being persisted. For that reason, the process will not be replicated in the present document.

With all the automatic configurations performed by GCN analyzed, it is important to check its logs by executing the following docker command:

```console
docker logs gcn
```

Which should yield a result similar to the following:

```console
boot - 2021-03-31 16:05:01,386 - [DEBUG] - logs startup successful.
cgn - 2021-03-31 16:05:01,836 - [INFO] - Logging system initialized.
cgn - 2021-03-31 16:05:01,836 - [INFO] - Application starting.
cgn - 2021-03-31 16:05:01,836 - [INFO] - Imported configuration:
cb_endpoint: http://orion:1026
cygnus_endpoint: http://cygnus:5051
iota_endpoint: http://iot-agent:4041
iota_protocol: MQTT
protocol_broker_address: mosquitto
protocol_broker_port: 1883
entity_id: urn:ngsi-ld:ImageRecord:001
camera_id:
api_key: camera
service: production
service_path: /manufacturer
sink: mongo
sink_endpoint: mongodb://mongo-db:27017
camera_name: urn:ngsi-ld:Camera:001
cgn - 2021-03-31 16:05:01,837 - [INFO] - Orion purge process started.
cgn - 2021-03-31 16:05:01,843 - [INFO] - Configuring entities at Orion and data persistency at Cygnus.
cgn - 2021-03-31 16:05:01,894 - [INFO] - [Orion]: Entity successfully created with the id urn:ngsi-ld:ImageRecord:001.
cgn - 2021-03-31 16:05:02,210 - [INFO] - [Orion]: The entity urn:ngsi-ld:ImageRecord:001 now has data persistence configured.
cgn - 2021-03-31 16:05:02,281 - [INFO] - [IoTA]: Service successfully created with the ApiKey camera.
cgn - 2021-03-31 16:05:04,643 - [INFO] - [IoTA]: Device successfully created with the id urn:ngsi-ld:Camera:001.
cgn - 2021-03-31 16:05:04,643 - [INFO] - Successful.
cgn - 2021-03-31 16:05:04,644 - [INFO] - Configuring database access.
cgn - 2021-03-31 16:05:04,647 - [DEBUG] - Database and container configured.
cgn - 2021-03-31 16:05:04,647 - [INFO] - Successful.
cgn - 2021-03-31 16:05:04,647 - [INFO] - Importing user camera module.
cgn - 2021-03-31 16:05:04,647 - [INFO] - Successful.
cgn - 2021-03-31 16:05:04,647 - [INFO] - Initializing the camera engine and connecting to the camera.
DEBUG CONNECT
DEBUG INITIALIZE
cgn - 2021-03-31 16:05:04,648 - [INFO] - Successful.
cgn - 2021-03-31 16:05:04,648 - [INFO] - Connecting to the MQTT and making device functions available.
cgn - 2021-03-31 16:05:04,651 - [INFO] - [MQTT]: Connected to broker.
```

Analyzing the presented content, it is possible to understand that all the elements that comprise GCN are sequentially configured. The most important note to take from this log record is the `DEBUG CONNECT` and `DEBUG INITIALIZE` that were previously defined in the `camera.py` file for the `connect` and `initialize` functions respectively. This proves that the code defined for the example is executed successfully for these functions, simulating a connection to a camera and initialization of its intrinsic parameters.

Considering the interaction between Orion and JSON IoT Agent, as [explained with detail in Fiware documentation](https://fiware-tutorials.readthedocs.io/en/latest/iot-agent-json/index.html#enabling-context-broker-commands), a capture command will now be issued to the camera through Orion using a HTTP request:

```http
### Issue a capture command to the camera through Orion
PATCH http://localhost:1026/v2/entities/urn:ngsi-ld:Camera:001/attrs
Content-Type: application/json
fiware-service: production
fiware-servicepath: /manufacturer

{
    "capture": {
        "type": "command",
        "value": ""
    }
}
```

The value parameter is irrelevant since it will not be processed, so it can be an empty `string`. The response should be as follows:

```http
HTTP/1.1 204 No Content
Connection: close
Content-Length: 0
Fiware-Correlator: 0f55fc02-923b-11eb-8d97-0242ac120104
Date: Wed, 31 Mar 2021 16:06:32 GMT
```

The HTTP code `204` states a successful operation without content. By executing the docker log command again for the `gcn` container:

```console
docker logs gcn
```

One should see that the following lines were added to the previously obtained logs:

```console
cgn - 2021-03-31 16:06:32,336 - [DEBUG] - [MQTT]: Message received:
Topic: /camera/urn:ngsi-ld:Camera:001/cmd
Message: b'{"capture":""}'
cgn - 2021-03-31 16:06:32,336 - [INFO] - [MQTT]: Capture command received.
DEBUG CAPTURE
DEBUG RETURN STRING: {"filename": "my_image1634", "image": "gASVKgEAAAAAAACMFW51bXB5LmNvcmUubXVsdGlhcnJheZSMDF9yZWNvbnN0cnVjdJSTlIwFbnVtcHmUjAduZGFycmF5lJOUSwCFlEMBYpSHlFKUKEsBSwJLCoaUaAOMBWR0eXBllJOUjAJpOJSJiIeUUpQoSwOMATyUTk5OSv////9K/////0sAdJRiiUOgAQAAAAAAAAABAAAAAAAAAAEAAAAAAAAAAQAAAAAAAAABAAAAAAAAAAEAAAAAAAAAAQAAAAAAAAABAAAAAAAAAAEAAAAAAAAAAQAAAAAAAAABAAAAAAAAAAEAAAAAAAAAAQAAAAAAAAABAAAAAAAAAAEAAAAAAAAAAQAAAAAAAAABAAAAAAAAAAEAAAAAAAAAAQAAAAAAAAABAAAAAAAAAJR0lGIu"}
cgn - 2021-03-31 16:06:38,350 - [DEBUG] - Image sent to database.
cgn - 2021-03-31 16:06:38,430 - [INFO] - [Orion] Image result entity updated.
cgn - 2021-03-31 16:06:38,430 - [INFO] - [MQTT]: Capture command issued.
```

The topic to which `gcn` is subscribed to, as can be seein in the message received log, respects the format `/<api-key>/<device-id>` to comply with the [JSON IoT Agent functionality](https://fiware-iotagent-json.readthedocs.io/en/latest/index.html). From this point on, the logging system shows the feedback for the code previously defined at the `camera.py` file for the `capture` command, yielding the results for the two `print` statements. One very important note is the fact that the [NumPy](https://numpy.org/) was successfully encoded into a string, as it can be seen in the value assigned to the `image` key of the `json` to be sent to the database.

To conclude the assessment of the success for the `capture` command, an access to the MongoDB instance needs to be performed in order to understand is the image was properly stored. As already mentioned, Fiware provides a detailed [step-by-step guide](https://fiware-tutorials.readthedocs.io/en/latest/historic-context-flume/index.html#mongodb-reading-data-from-a-database) on how to perform such task. Here, only the commands executed inside the MongoDB container will be presented, and the first one is to list the databases:

```console
show dbs
```

Yielding the result:

```console
admin             0.000GB
config            0.000GB
iotagentjson      0.000GB
local             0.000GB
orion             0.000GB
orion-production  0.000GB
production        0.000GB
sth_default       0.000GB
```

The `production` database, defined as the `service` parameter at the `configuration.json` file, is successfully created. The next step is to list the corresponding database collections:

```console
use production
show collections
```

Which yields the following result:

```console
/manufacturer.chunks
/manufacturer.files
```

The `manufacturer` collection, defined as the `service-path` at the `configuration.json` file, is successfully created. Since `gcn` uses [GridFS](https://docs.mongodb.com/manual/core/gridfs/) to store files, these are split into chunks and saved in the auxiliary `/manufacturer.chunks` collection, while all the metadata is stored at the `/manufacturer.files`. These collections cooperate in MongoDB internal processes so that the user, when consuming data from MongoDB, only needs to know that the `/manufacturer` collection is available and has files in it.

To list the first 10 files of the collection (hopefully there is only one at the current stage):

```console
db["/manufacturer.files"].find().limit(10);
```

Which yields:

```console
{ "_id" : ObjectId("60649e0d78ad6db8940f9938"), "encoding" : "utf-8", "filename" : "my_image1634", "md5" : "546d0d322d20bfbfb7d2e887b8287fb8", "chunkSize" : 261120, "length" : NumberLong(412), "uploadDate" : ISODate("2021-03-31T16:06:38.348Z") }
```

It is possible to confirm that the file metadata is correct, namely the `filename`, by comparing with the `print` statement results produced by the `camera.py` `capture` function. One can argue that the content of the file is not being presented. In orded to do so, and due to the operation principle of [GridFS](https://docs.mongodb.com/manual/core/gridfs/), it is necessary to query the `/manufacturer.chunks` collection to actually see the saved image content:

```console
db["/manufacturer.chunks"].find().limit(10);
```

Yielding:

```console
{ "_id" : ObjectId("60649e0e78ad6db8940f9939"), "files_id" : ObjectId("60649e0d78ad6db8940f9938"), "n" : 0, "data" : BinData(0,"Z0FTVktnRUFBQUFBQUFDTUZXNTFiWEI1TG1OdmNtVXViWFZzZEdsaGNuSmhlWlNNREY5eVpXTnZibk4wY25WamRKU1RsSXdGYm5WdGNIbVVqQWR1WkdGeWNtRjVsSk9VU3dDRmxFTUJZcFNIbEZLVUtFc0JTd0pMQ29hVWFBT01CV1IwZVhCbGxKT1VqQUpwT0pTSmlJZVVVcFFvU3dPTUFUeVVUazVPU3YvLy8vOUsvLy8vLzBzQWRKUmlpVU9nQVFBQUFBQUFBQUFCQUFBQUFBQUFBQUVBQUFBQUFBQUFBUUFBQUFBQUFBQUJBQUFBQUFBQUFBRUFBQUFBQUFBQUFRQUFBQUFBQUFBQkFBQUFBQUFBQUFFQUFBQUFBQUFBQVFBQUFBQUFBQUFCQUFBQUFBQUFBQUVBQUFBQUFBQUFBUUFBQUFBQUFBQUJBQUFBQUFBQUFBRUFBQUFBQUFBQUFRQUFBQUFBQUFBQkFBQUFBQUFBQUFFQUFBQUFBQUFBQVFBQUFBQUFBQUFCQUFBQUFBQUFBSlIwbEdJdQ==") }
```

A direct comparison with the image content generated by the `camera.py` `capture` function is not possible due to automatic conversions to binary format performed by MongoDB, but it is clear that there is content, and it is associated to the same `ObjectId` in both the `/manufacturer.chunks` and `/manufacturer.files` collections.

As an example, another camera capture is issued:

```http
### Issue a capture command to the camera through Orion
PATCH http://localhost:1026/v2/entities/urn:ngsi-ld:Camera:001/attrs
Content-Type: application/json
fiware-service: production
fiware-servicepath: /manufacturer

{
    "capture": {
        "type": "command",
        "value": ""
    }
}
```

The `gcn` logs are consulted:

```console
docker logs gcn
```

Adding to the previous logs:

```console
cgn - 2021-03-31 16:09:04,177 - [DEBUG] - [MQTT]: Message received:
Topic: /camera/urn:ngsi-ld:Camera:001/cmd
Message: b'{"capture":""}'
cgn - 2021-03-31 16:09:04,178 - [INFO] - [MQTT]: Capture command received.
DEBUG CAPTURE
DEBUG RETURN STRING: {"filename": "my_image14", "image": "gASVKgEAAAAAAACMFW51bXB5LmNvcmUubXVsdGlhcnJheZSMDF9yZWNvbnN0cnVjdJSTlIwFbnVtcHmUjAduZGFycmF5lJOUSwCFlEMBYpSHlFKUKEsBSwJLCoaUaAOMBWR0eXBllJOUjAJpOJSJiIeUUpQoSwOMATyUTk5OSv////9K/////0sAdJRiiUOgAQAAAAAAAAABAAAAAAAAAAEAAAAAAAAAAQAAAAAAAAABAAAAAAAAAAEAAAAAAAAAAQAAAAAAAAABAAAAAAAAAAEAAAAAAAAAAQAAAAAAAAABAAAAAAAAAAEAAAAAAAAAAQAAAAAAAAABAAAAAAAAAAEAAAAAAAAAAQAAAAAAAAABAAAAAAAAAAEAAAAAAAAAAQAAAAAAAAABAAAAAAAAAJR0lGIu"}
cgn - 2021-03-31 16:09:09,194 - [DEBUG] - Image sent to database.
cgn - 2021-03-31 16:09:09,210 - [INFO] - [Orion] Image result entity updated.
cgn - 2021-03-31 16:09:09,211 - [INFO] - [MQTT]: Capture command issued.
```

And a new query to MongoDB is performed:

```console
db["/manufacturer.files"].find().limit(10);
```

Resulting in:

```console
{ "_id" : ObjectId("60649e0d78ad6db8940f9938"), "encoding" : "utf-8", "filename" : "my_image1634", "md5" : "546d0d322d20bfbfb7d2e887b8287fb8", "chunkSize" : 261120, "length" : NumberLong(412), "uploadDate" : ISODate("2021-03-31T16:06:38.348Z") }
{ "_id" : ObjectId("60649ea578ad6db8940f993a"), "encoding" : "utf-8", "filename" : "my_image14", "md5" : "546d0d322d20bfbfb7d2e887b8287fb8", "chunkSize" : 261120, "length" : NumberLong(412), "uploadDate" : ISODate("2021-03-31T16:09:09.193Z") }
```

Where a brand new image, `my_image14`, is presented.

At this point, only the `configure` camera command is yet to be tested. To do so, an example `configure` command is issued using the same process of the `capture` command, but this time, the `value` parameter has relevance since it will be passed to the `configure` function defined at the `camera.py` file:

```http
### Issue a configuration command to the camera through Orion
POST http://localhost:1026/v2/op/update
Content-Type: application/json
fiware-service: production
fiware-servicepath: /manufacturer

{
    "actionType": "update",
    "entities": [
        {
            "id": "urn:ngsi-ld:Camera:001",
            "type": "camera",
            "configure": {
                "type": "command",
                "value": {
                    "brightness": 0.9,
                    "flash": "off",
                    "focus": "auto",
                    "filter": "none"
                }
            }
        }
    ]
}
```

>***Important note: bear in mind [Orion's forbidden characters](https://fiware-orion.readthedocs.io/en/master/user/forbidden_characters/index.html) when composing configuration structures or values.***
>***Important note: At the time of the `gcn` development, [Orion's batch update operation](https://fiware-tutorials.readthedocs.io/en/latest/crud-operations/index.html#update-operations) appears to be the only available way to send command values through the IoT Agent. This may be explained due to the change from NGSIv1 specification to NGSIv2, and the reason why this happens is beyond the scope of the present document. This note aims only to justify the reason why the `capture` command is composed with a different structure from the `configure` command. Nonetheless, all the desired functionality is achieved.***

Orion answers with a success code without content:

```http
HTTP/1.1 204 No Content
Connection: close
Content-Length: 0
Fiware-Correlator: b983fd3c-923b-11eb-891b-0242ac120104
Date: Wed, 31 Mar 2021 16:11:17 GMT
```

By accessing `gcn` logs once again:

```console
docker logs gcn
```

One should see that the following lines were appended to the existing logs:

```console
cgn - 2021-03-31 16:11:17,837 - [DEBUG] - [MQTT]: Message received:
Topic: /camera/urn:ngsi-ld:Camera:001/cmd
Message: b'{"configure":{"brightness":0.9,"flash":"off","focus":"auto","filter":"none"}}'
cgn - 2021-03-31 16:11:17,838 - [INFO] - [MQTT]: Configuration command received.
DEBUG CONFIGURE {'brightness': 0.9, 'flash': 'off', 'focus': 'auto', 'filter': 'none'}
cgn - 2021-03-31 16:11:17,840 - [INFO] - [MQTT]: Configuration command issued.
cgn - 2021-03-31 16:11:17,840 - [DEBUG] - [MQTT]: Publishing device configuration update.
cgn - 2021-03-31 16:11:17,842 - [DEBUG] - [MQTT]: Device configuration update published.
```

Considering the `print` statements defined for the `configure` function at the `camera.py` file, it is possible to infer that the configuration task was executed as expected. Additionally, the parameters defined at the example were delivered to the `configure` function with the same structure that was presented to Orion through the HTTP request. 

The image data is persisting in the database, and the proper functionality of the camera device is tested, it is now time to query Orion for the [Image Reference Entity](./data_models/image_reference.json):

```http
### Get Orion Entities
GET http://localhost:1026/v2/entities
```

Resulting in:

```http
HTTP/1.1 200 OK
Connection: close
Content-Length: 262
Content-Type: application/json
Fiware-Correlator: e67cff1e-923b-11eb-869a-0242ac120104
Date: Wed, 31 Mar 2021 16:12:33 GMT

[
  {
    "id": "urn:ngsi-ld:ImageRecord:001",
    "type": "imageReference",
    "image": {
      "type": "reference",
      "value": {
        "databaseType": "mongo",
        "databaseEndpoint": "mongodb://mongo-db:27017",
        "database": "production",
        "collection": "/manufacturer",
        "imageFile": "my_image14"
      },
      "metadata": {}
    }
  }
]
```

Where the most recent obtained image, `my_image14`, is properly presented as the `imageFile` parameter value.

Regarding the device entity:

```http
### Device entities at production service and manufacturer service-path
GET http://localhost:1026/v2/entities
fiware-service: production
fiware-servicepath: /manufacturer
```

Presents the result:

```http
HTTP/1.1 200 OK
Connection: close
Content-Length: 1033
Content-Type: application/json
Fiware-Correlator: f4ef1eec-923b-11eb-9b14-0242ac120104
Date: Wed, 31 Mar 2021 16:12:57 GMT

[
  {
    "id": "urn:ngsi-ld:Camera:001",
    "type": "camera",
    "TimeInstant": {
      "type": "DateTime",
      "value": "2021-03-31T16:11:17.00Z",
      "metadata": {}
    },
    "capture_info": {
      "type": "commandResult",
      "value": "true",
      "metadata": {
        "TimeInstant": {
          "type": "DateTime",
          "value": "2021-03-31T16:09:09.00Z"
        }
      }
    },
    "capture_status": {
      "type": "commandStatus",
      "value": "OK",
      "metadata": {
        "TimeInstant": {
          "type": "DateTime",
          "value": "2021-03-31T16:09:09.00Z"
        }
      }
    },
    "configuration": {
      "type": "String",
      "value": {
        "brightness": 0.9,
        "flash": "off",
        "focus": "auto",
        "filter": "none"
      },
      "metadata": {
        "TimeInstant": {
          "type": "DateTime",
          "value": "2021-03-31T16:11:17.00Z"
        }
      }
    },
    "configure_info": {
      "type": "commandResult",
      "value": {
        "brightness": 0.9,
        "flash": "off",
        "focus": "auto",
        "filter": "none"
      },
      "metadata": {
        "TimeInstant": {
          "type": "DateTime",
          "value": "2021-03-31T16:11:17.00Z"
        }
      }
    },
    "configure_status": {
      "type": "commandStatus",
      "value": "OK",
      "metadata": {
        "TimeInstant": {
          "type": "DateTime",
          "value": "2021-03-31T16:11:17.00Z"
        }
      }
    },
    "capture": {
      "type": "command",
      "value": "",
      "metadata": {}
    },
    "configure": {
      "type": "command",
      "value": "",
      "metadata": {}
    }
  }
]
```

It shows the command status attributes with the `OK` value and timestamps that match the ones presented by the `gcn` logs. Additionally, the `configuration` attribute shows the parameters that were used in the present example, stating that those are the actual parameters configured for the camera (although in reality all that was done was a `print` function).

From this point on, it is possible to make use of a configurable camera which will have all of its images stored in a database service and present all the relevant context data at Orion, allowing other services to consume this information as needed. One example of such services is the [ICN - Image Classification Node](../icn/README.md) designed to ideally work together with GCN composing a system which can be interpreted as a Vision-Based Classification System as described in the [FIREFIT RoseAP repository documentation](../README.md).

