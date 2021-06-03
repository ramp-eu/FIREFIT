# ICN - Image Classification Node

The [Image Classification Node (ICN)](../) aims to easily integrate Machine Learning or Deep Learning models to perform **image classification** tasks into a [FIWARE](https://fiware-tutorials.readthedocs.io/en/latest/index.html) solution, abstracting the user fom entity, device, database and data persistency configurations.

## How to build the images

The procedures to build an image for the [ICN](../) are presented in the [Installation and Administration Guide](../docs/installationguide.md).

## How to use the images

Once instantiated, the [ICN](../) must connect to an instance of the [Orion Context Broker](https://fiware-orion.readthedocs.io/en/latest/). A sample [`docker-compose`](docker-compose.yml) file is provided.

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

  # GCN (tensorflow)
  gcn:
    image: introsyspt/gcn:tensorflow
    hostname: gcn
    container_name: gcn
    depends_on:
        - orion
        - iot-agent
        - mosquitto
        - mongo-db
    networks:
        - default

  # ICN
  icn:
    image: introsyspt/icn
    hostname: icn
    container_name: icn
    depends_on:
        - orion
        - iot-agent
        - mosquitto
        - mongo-db
    networks:
        - default
    expose:
        - "8181"
    ports:
        - "8181:8181"

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

- [Orion](https://fiware-orion.readthedocs.io/en/latest/) - `orion:1026`
- [MongoDB](https://www.mongodb.com/) - `mongo-db:27017`
- [JSON IoT Agent](https://fiware-iotagent-json.readthedocs.io/en/latest/) - `iot-agent:4041`
- [Mosquitto](https://mosquitto.org/) (MQTT broker) - `mosquitto:1883`
- [Cygnus](https://fiware-cygnus.readthedocs.io/en/latest/) - `cygnus:5051`

Please refer to the [documentation](../docs) for further configuration information.
