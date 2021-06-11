# Getting Started

In this section, a [GCN](https://github.com/Introsys/FIREFIT.ROSE-AP/tree/master/gcn) usage example is presented.

> ***Be aware that the following content should be used as a reference only and not as a production ready solution. There are several security concerns that should be taken into account depending on the context where CGN will operate.***

## Introduction

In order to produce the same results as presented here, it is advised to use [Visual Studio Code](https://code.visualstudio.com/) with the [REST Client extension](https://github.com/Huachao/vscode-restclient) to perform HTTP requests.

As a starting point, it is important to understand which services are necessary to ensure the [GCN](https://github.com/Introsys/FIREFIT.ROSE-AP/tree/master/gcn) functionality, as mentioned in the [Installation and Administration Guide](installationguide.md). For this reason, the following `docker-compose.yml` file represents the deployment of the present example:

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
    volumes:
      - type: bind
        source: ./mosquitto/config
        target: /mosquitto/config
  
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
    image: introsyspt/gcn
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

- [Orion](https://fiware-orion.readthedocs.io/en/master/) - `orion:1026`
- [MongoDB](https://www.mongodb.com/) - `mongo-db:27017`
- [JSON IoT Agent](https://fiware-iotagent-json.readthedocs.io/en/latest/) - `iot-agent:4041`
- [Mosquitto](https://mosquitto.org) (MQTT broker) - `mosquitto:1883`
- [Cygnus](https://fiware-cygnus.readthedocs.io/en/latest/) - `cygnus:5051`

For this getting started example, a default [configuration](https://github.com/Introsys/FIREFIT.ROSE-AP/blob/master/gcn/configuration/configuration.json) is provided, according to the following:

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

A detailed explanation of each parameter and how to configure the [GCN](https://github.com/Introsys/FIREFIT.ROSE-AP/tree/master/gcn) and build a local docker image with the new configuration is given in the [Installation and Administration Guide](installationguide.md).

By comparing with the `docker-compose`, it is possible to quickly correlate the defined parameters with the `hostname` and exposed/configured ports of each service.

The id `urn:ngsi-ld:ImageRecord:001` will be assigned to the [Image Reference Entity](https://github.com/Introsys/FIREFIT.ROSE-AP/blob/master/gcn/data_models/image_reference.json) that will be created at [Orion](https://fiware-orion.readthedocs.io/en/master/).

The id `urn:ngsi-ld:Camera:001` will be assigned to the camera device that will be created at [Orion](https://fiware-orion.readthedocs.io/en/master/) through [JSON IoT Agent](https://fiware-iotagent-json.readthedocs.io/en/latest/stepbystep/index.html).

Each image obtained from the camera will be stored at the `manufacturer` collection of the `production` database from a [MongoDB](https://www.mongodb.com/) instance (`mongo` defined as `sink`).

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

## Initialize the stack

To initialize the stack, use the provided [`docker-compose`](https://github.com/Introsys/FIREFIT.ROSE-AP/blob/master/gcn/docker/docker-compose.yml) file by issuing the commands:

```console
git clone https://github.com/Introsys/FIREFIT.ROSE-AP.git
cd FIREFIT.ROSE-AP/gcn/docker

docker-compose -p gcn_stack up -d
```

> **Note:** a mosquitto configuration file must be present enabling remote client access.

This should create all the service instances. By checking the running containers:

```console
docker container ls --all
```

One should obtain the following result:

```console
CONTAINER ID   IMAGE                         COMMAND                  CREATED          STATUS          PORTS                              NAMES
50d8262d9537   introsyspt/gcn                "python ./cgn.py"        11 minutes ago   Up 11 minutes                                      gcn
8b7467ef977a   fiware/cygnus-ngsi:latest     "/cygnus-entrypoint.…"   11 minutes ago   Up 11 minutes   5050/tcp, 5080/tcp                 fiware-cygnus
0212052b2e2e   fiware/orion:2.4.0            "/usr/bin/contextBro…"   11 minutes ago   Up 11 minutes   0.0.0.0:1026->1026/tcp             fiware-orion
72bbe96da225   fiware/iotagent-json:latest   "docker/entrypoint.s…"   11 minutes ago   Up 11 minutes   0.0.0.0:4041->4041/tcp, 7896/tcp   fiware-iot-agent
3aa2f8d41d86   eclipse-mosquitto             "/docker-entrypoint.…"   11 minutes ago   Up 11 minutes   0.0.0.0:1883->1883/tcp             mosquitto
3b2cc0820f9d   mongo:3.6                     "docker-entrypoint.s…"   11 minutes ago   Up 11 minutes   0.0.0.0:27017->27017/tcp           db-mongo
```

If you want to clean up and start again you can do so with the following command:

```console
docker-compose -p gcn_stack down
```

## Querying context data

Using [Visual Studio Code](https://code.visualstudio.com/) with the [REST Client extension](https://github.com/Huachao/vscode-restclient), it is possible to query [Orion](https://fiware-orion.readthedocs.io/en/master/) for its entities:

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

The only existing entity is the [Image Reference Entity](https://github.com/Introsys/FIREFIT.ROSE-AP/blob/master/gcn/data_models/image_reference.json), confirming that it was successfully configured as a context entity with the configured id `urn:ngsi-ld:ImageRecord:001`. The successful creation of the camera device entity is yet to be confirmed, and to do so, the `service` and `service-path` need to be considered when querying [Orion](https://fiware-orion.readthedocs.io/en/master/):

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

One can infer that the device configuration was successfully performed, having the camera device available with the `capture` and `configure` commands as well as the `configuration` attribute stating the current configuration of the device. The configured id `urn:ngsi-ld:Camera:001` is also confirmed.

## Check devices defined by the IoT Agent

Since the device was created at [Orion](https://fiware-orion.readthedocs.io/en/master/) through an intrinsic mechanism of [JSON IoT Agent](https://fiware-iotagent-json.readthedocs.io/en/latest/stepbystep/index.html), it is possible to query the Agent to validate that the same representation of the device is defined, note the distinct address to where the HTTP request is sent:

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

The same device structure is presented, an expected result since it is the [JSON IoT Agent](https://fiware-iotagent-json.readthedocs.io/en/latest/stepbystep/index.html) the one responsible for creating the device entity at [Orion](https://fiware-orion.readthedocs.io/en/master/).

## Check the API key defined by the IoT agent

Another important query to [JSON IoT Agent](https://fiware-iotagent-json.readthedocs.io/en/latest/stepbystep/index.html) will determine if the proper `api_key` was defined, it is an important element since it will define part of the `MQTT` topics to which the IoT Agent will publish and subscribe to:

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

One can infer that the `api_key`, `service` and `service-path` defined at the [`configuration.json`](https://github.com/Introsys/FIREFIT.ROSE-AP/blob/master/gcn/configuration/configuration.json) are properly defined as a service, a mechanism used by [JSON IoT Agent](https://fiware-iotagent-json.readthedocs.io/en/latest/stepbystep/index.html).

## Check data persistency

The only remaining element that is yet to be confirmed regarding [Orion](https://fiware-orion.readthedocs.io/en/master/) is the [Image Reference Entity](https://github.com/Introsys/FIREFIT.ROSE-AP/blob/master/gcn/data_models/image_reference.json) data persistency. To do so, a query to [Orion](https://fiware-orion.readthedocs.io/en/master/)'s subscriptions will be performed:

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

This confirms that [Orion](https://fiware-orion.readthedocs.io/en/master/) is notifying the [Cygnus](https://fiware-cygnus.readthedocs.io/en/latest/) service regarding changes to the [Image Reference Entity](https://github.com/Introsys/FIREFIT.ROSE-AP/blob/master/gcn/data_models/image_reference.json).

> **Note:** FIWARE provides a detailed [step-by-step guide](https://fiware-tutorials.readthedocs.io/en/latest/historic-context-flume/index.html#mongodb-reading-data-from-a-database) on how to confirm that data is being persisted. For that reason, the process will not be replicated in the present document.

## Get log data

With all the automatic configurations performed by [GCN](https://github.com/Introsys/FIREFIT.ROSE-AP/tree/master/gcn) analyzed, it is important to check its logs by executing the following docker command:

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

Analyzing the presented content, it is possible to understand that all the elements that comprise [GCN](https://github.com/Introsys/FIREFIT.ROSE-AP/tree/master/gcn) are sequentially configured. The most important note to take from this log record is the `DEBUG CONNECT` and `DEBUG INITIALIZE` that were previously defined in the `camera.py` file for the `connect` and `initialize` functions respectively. This proves that the code defined for the example is executed successfully for these functions, simulating a connection to a camera and initialization of its intrinsic parameters.

## Issue a capture command to the camera through Orion

Considering the interaction between [Orion](https://fiware-orion.readthedocs.io/en/master/) and [JSON IoT Agent](https://fiware-iotagent-json.readthedocs.io/en/latest/stepbystep/index.html), as explained with detail in [FIWARE documentation](https://fiware-tutorials.readthedocs.io/en/latest/iot-agent-json/index.html#enabling-context-broker-commands), a capture command will now be issued to the camera through [Orion](https://fiware-orion.readthedocs.io/en/master/) using a HTTP request:

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

The topic to which `gcn` is subscribed to, as can be seen in the message received log, respects the format `/<api-key>/<device-id>` to comply with the [JSON IoT Agent functionality](https://fiware-iotagent-json.readthedocs.io/en/latest/index.html). From this point on, the logging system shows the feedback for the code previously defined at the `camera.py` file for the `capture` command, yielding the results for the two `print` statements. One very important note is the fact that the [NumPy](https://numpy.org/) was successfully encoded into a string, as it can be seen in the value assigned to the `image` key of the `json` to be sent to the database.

To conclude the assessment of the success for the `capture` command, an [access to the MongoDB](https://fiware-tutorials.readthedocs.io/en/latest/historic-context-flume/index.html#mongodb-reading-data-from-a-database) instance needs to be performed in order to understand if the image was properly stored.

To do so, first attach a shell session to the running instance of MongoDB container:

```console
docker exec -i -t db-mongo /bin/bash
```

You can then log into to the running mongo-db database:

```console
mongo --host mongo-db
```

Finally, list the available databases:

```console
show dbs
```

The result should be as follows:

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

The `manufacturer` collection, defined as the `service-path` at the `configuration.json` file, is successfully created. Since `gcn` uses [GridFS](https://docs.mongodb.com/manual/core/gridfs/) to store files, these are split into chunks and saved in the auxiliary `/manufacturer.chunks` collection, while all the metadata is stored at the `/manufacturer.files`. These collections cooperate in [MongoDB](https://www.mongodb.com/) internal processes so that the user, when consuming data from [MongoDB](https://www.mongodb.com/), only needs to know that the `/manufacturer` collection is available and has files in it.

To list the first 10 files of the collection (hopefully there is only one at the current stage):

```console
db["/manufacturer.files"].find().limit(10);
```

Which yields:

```console
{ "_id" : ObjectId("60649e0d78ad6db8940f9938"), "encoding" : "utf-8", "filename" : "my_image1634", "md5" : "546d0d322d20bfbfb7d2e887b8287fb8", "chunkSize" : 261120, "length" : NumberLong(412), "uploadDate" : ISODate("2021-03-31T16:06:38.348Z") }
```

It is possible to confirm that the file metadata is correct, namely the `filename`, by comparing with the `print` statement results produced by the `camera.py` `capture` function. One can argue that the content of the file is not being presented. In order to do so, and due to the operation principle of [GridFS](https://docs.mongodb.com/manual/core/gridfs/), it is necessary to query the `/manufacturer.chunks` collection to actually see the saved image content:

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

Where a  new image, `my_image14`, is presented.

## Issue a configuration command to the camera through Orion

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

[Orion](https://fiware-orion.readthedocs.io/en/master/) answers with a success code without content:

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

Considering the `print` statements defined for the `configure` function at the `camera.py` file, it is possible to infer that the configuration task was executed as expected. Additionally, the parameters defined at the example were delivered to the `configure` function with the same structure that was presented to [Orion](https://fiware-orion.readthedocs.io/en/master/) through the HTTP request.

The image data is persisting in the database, and the proper functionality of the camera device is tested, it is now time to query [Orion](https://fiware-orion.readthedocs.io/en/master/) for the [Image Reference Entity](https://github.com/Introsys/FIREFIT.ROSE-AP/blob/master/gcn/data_models/image_reference.json):

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

From this point on, it is possible to make use of a configurable camera which will have all of its images stored in a database service and present all the relevant context data at [Orion](https://fiware-orion.readthedocs.io/en/master/), allowing other services to consume this information as needed. One example of such services is the [ICN - Image Classification Node](https://github.com/Introsys/FIREFIT.ROSE-AP/tree/master/icn) designed to ideally work together with GCN composing a system which can be interpreted as a Vision-Based Classification System as described by the [FIREFIT ROSE-AP](https://github.com/Introsys/FIREFIT.ROSE-AP).

---

**Previous:** [Installation and Administration Guide](installationguide.md) | **Next:** [User Manual](usermanual.md)
