# GCN - Generic Camera Node

The [GCN](../) is a component that aims to easily integrate any generic camera into a FIWARE solution, abstracting the user from entity, device, database and data persistency configurations. It provides the image capture and camera configuration functionalities, and also ensures the obtained images data persistency to a user-defined database service.

## How to build the images

The procedures to build an image for the [GCN](../) are presented in the [Installation and Administration Guide](../docs/installationguide.md).

## How to use the images

Once instantiated, the [GCN](../) must connect to an instance of the [Orion Context Broker](https://fiware-orion.readthedocs.io/en/latest/). A sample [`docker-compose`](docker-compose.yml) file is provided.

```yml
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
        - "7896"
    ports:
        - "4041:4041"
        - "7896:7896"
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
    expose:
        - "5080"
    ports:
        - "5051:5051"
        - "5080:5080"
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

Please refer to the [documentation](../gcn/docs) for further configuration information.
