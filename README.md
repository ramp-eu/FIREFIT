# FIREFIT ROSE-AP

[![License: AGPL-3.0](https://img.shields.io/github/license/ramp-eu/TTE.project1.svg)](https://opensource.org/licenses/AGPL-3.0)
[![Docker badge](https://img.shields.io/docker/pulls/ramp-eu/TTE.project1.svg)](https://hub.docker.com/repository/docker/magnoguedes/firefit-rose-ap)
[![Documentation Status](https://readthedocs.org/projects/firefitrose-ap/badge/?version=latest)](https://firefitrose-ap.readthedocs.io/en/latest/?badge=latest)
[![CII Best Practices](https://bestpractices.coreinfrastructure.org/projects/4832/badge)](https://bestpractices.coreinfrastructure.org/projects/4832)

The present repository holds the FIREFIT ROSE-AP components proposed by [Introsys](https://www.introsys.eu/?lang=en) which aim to easily integrate generic cameras and image classification processes into a [FIWARE](https://www.fiware.org/) solution, abstracting the user from concerns such as entity configuration, data persistency, device configuration or database configuration.

This project is part of [DIH^2](http://www.dih-squared.eu/). For more information check the RAMP Catalogue entry for the [components](https://github.com/xxx).

| :books: [Documentation](https://firefitrose-ap.readthedocs.io/en/latest/) |:whale: [Docker Hub](https://hub.docker.com/repository/docker/magnoguedes/firefit-rose-ap) | :camera: [GCN](gcn) | :mag: [ICN](icn)
| --- | --- | --- | --- |

## Contents

- [Background](#background)
- [Install](#install)
- [Usage](#usage)
- [API](#api)
- [License](#license)

## Background

This ROSE-AP solution is composed by two main components:

- The [Generic Camera Node (GCN)](gcn) enables simple integration of industrial cameras in the FIWARE ecosystem.
- The [Image Classification Node (ICN)](icn) was designed to facilitate the development and integration of image processing algorithms and machine learning tools for feature classification in images.

Due to their [synergy](#synergy-between-the-gcn-and-icn), it is possible to consider that any solution implementing the components herein presented is making use of a Vision-based Inspection System. Although this classification depends on the application, it is relevant in the context where ROSE-AP stands, since it was designed as an answer to requirements and optimizations imposed and identified by the [FIREFIT experiment](http://www.dih-squared.eu/TTE-FIREFIT).

The [flexibility](#flexibility) offered by these components relies heavily in the usage of [Python](https://www.python.org/), an increasingly popular programming language commonly used in Machine Learning and Deep Leaning contexts and hardware communication.

### GCN

The Generic Camera Node aims to easily integrate any type of camera into FIWARE context as long as the necessary mechanisms to operate it can be programmed in [Python](https://www.python.org/).

Although a more detailed explanation is presented in the [corresponding repository documentation](gcn/docs), in short terms, the GCN performs the following tasks:

- creates an [Image Reference Entity](gcn/data_models/image_reference.json) directly at Orion and the corresponding data persistence at MongoDB through Cygnus,
- creates a representation of the camera as a device at Orion through the IoT Agent with configuration and actuation available,
- creates a database instance at MongoDB to store the obtained images,
- updates the [Image Reference Entity](gcn/data_models/image_reference.json) registered at Orion with a new image reference each time the camera captures and stores a new image.

This results in a device entity becoming available at Orion and to which the user can send configuration and capture commands. At each capture, the obtained image is automatically stored at the database and the [Image Reference Entity](gcn/data_models/image_reference.json) is updated with the corresponding information. At each configuration command, the processes defined by the user are performed and the device context is also updated at Orion.

Additional information regarding this component is presented in the [corresponding repository documentation](gcn/docs).

### ICN

The Image Classification Node aims to easily integrate image classification algorithms into FIWARE context as long as the necessary elements can be programmed in [Python](https://www.python.org/).

Although a more detailed explanation is presented in the [corresponding repository documentation](icn/docs), in short terms, the ICN performs the following tasks:

- creates an [Classification Result Entity](.icn/data_models/classification_result.json) directly at Orion and the corresponding data persistence at MongoDB through Cygnus,
- creates a classifier device at Orion through the IoT Agent with classification and model selection functionalities available,
- consumes images from a database,
- consumes models from a model database,
- performs automatic image classification by subscribing to entity changes as long as the entity respects the [Image Reference Entity](gcn/data_models/image_reference.json) datamodel (also created by GCN),
- updates the device command status to `PENDING` when making use of the subscription entity, since it does not go through the IoT Agent,
- updates the [Classification Result Entity](icn/data_models/classification_result.json) registered at Orion with a new result each time a classification is performed.

This results in a device entity becoming available at Orion and to which the user can send classification and model selection commands. Prior to the classification task, a machine learning/deep learning model is consumed from the specified database and set as the currently active model. Being now able to classify images, the ICN will then consume images from the specified database each time there is an entity update or the user commands it to do so, classifies the image, and updates the [Classification Result Entity](icn/data_models/classification_result.json) with the newly obtained result. It also allows the user to list the available models so that a new one can be defined as the active model.

Additional information regarding this component is presented in the [corresponding repository documentation](icn/docs).

### Synergy between the GCN and ICN

Although the GCN and ICN can be used as standalone components they were designed to work together, composing a Vision-based classification system or, in the context of the [FIREFIT experiment](http://www.dih-squared.eu/TTE-FIREFIT), a **Vision-based inspection system**.

To better understand how these components cooperate, an implementation example is presented in the following image:s

<div>
  <p align="center">
    <img src="system.png">
  </p>
  <p align="center">Vision-based Inspection System</p>
</div>

The first thing to note is that all the data persistency of Orion entities is taken care by Cygnus and all the MQTT messaging is going through Mosquitto, these elements are not represented for the sake of simplicity.

Having a camera device defined by GCN available at Orion, the starting point of system operation comes from a capture command provided by the user or any user-defined service. That command is translated into a MQTT message by the JSON IoT Agent and sent to GCN. The capture operation is performed according to the logic provided by the user and the obtained image is stored into the image database service, concluding with a MQTT confirmation message stating the success. At the same time,the GCN will send a direct HTTP message to Orion to have the corresponding [Image Reference Entity](gcn/data_models/image_reference.json) updated with the most recent information. The JSON IoT Agent is aware of the MQTT confirmation message and will update the status of the device capture command.

As soon as the [Image Reference Entity](gcn/data_models/image_reference.json) is updated, the ICN will be notified and will receive the corresponding content. In it, the image storage location is specified, allowing ICN to access the image database service and grab the newly created image. Having the image available, the user-defined classification process is then carried out using a Machine Learning or Deep Learning model previously selected by the user and obtained from the model database service. Since this process was triggered by the Orion subscription mechanism there was no classification command issued through JSON IoT Agent, for that reason the classifier device never got the opportunity to update its classification command status to `PENDING`, a task performed by the JSON IoT Agent. The ICN fills this gap by producing the same behavior expected from JSON IoT Agent ensuring that the classifier device has its classification command status properly updated to `PENDING` together with the corresponding timestamp. From this process, a string stating the result of the classification is associated to the image, composing the necessary information to update the [Classification Result Entity](icn/data_models/classification_result.json) through a HTTP message sent directly to Orion. At the same time, a MQTT command confirmation message is published, being this time the JSON IoT Agent the one responsible to update the classification command status of the classifier device.

This way, with a simple camera capture command, a whole process of image capture, storage and classification is automatically performed, ensuring all the data persistency, status update and the flexibility to select models according to each need, abstracting the user from complex configurations necessary to interact with FIWARE and Third-party components.

### Flexibility

In this section a brief description of the flexibility offered by each of the proposed components is presented, more information is provided at each corresponding repository documentation.

The GCN component allows users to program the processes of capture and configuration of the cameras they wish to integrate as long as [Python](https://www.python.org/) is used. It is up to the user to define how the communication to the camera is established, how it is configured and how the capture operation is performed. This allows users to use any type of communication protocol, manufacturer specific libraries and camera specific parameterization. Since these processes are defined in [Python](https://www.python.org/), any additional libraries can be imported and used. Although all the typical functionality of a generic device is ensured through the JSON IoT Agent, the user can also operate this component through direct MQTT messages, always considering that the device entity will not have its command attributes updated to `PENDING` status.

The ICN component allows users to program the image classification process as long as [Python](https://www.python.org/) is used. It is up to the user to define the model loading, image preprocessing and image classification processes. This allows users to use any library and pipeline as long as they are compatible with [Python](https://www.python.org/). The image subject to classification is provided automatically by the component since it is consumed from the image database service. Regarding the model usage, this component only makes use of existing machine learning/deep learning models stored in the model database service. It allows the user to list and select the desired model but it is up to the user to ensure the instantiation of the model. Although all the typical functionality of a generic device is ensured through the JSON IoT Agent, the user can also operate this component through direct MQTT messages, always considering that the device entity will not have its command attributes updated to `PENDING` status.

It is imperative that all the necessary structures and usage condition is respected, as specified in the  documentation.

### Introsys

[Introsys](https://www.introsys.eu/?lang=en) is a technology provider and system integrator company dedicated on the creation of customized solutions for automation, control systems and quality inspection.

### FIWARE

[FIWARE](https://www.fiware.org/) is a curated framework of open source platform components which can be assembled together and with other third-party platform components to accelerate the development of Smart Solutions.

## Install

Information about how to install the FIREFIT ROSE-AP components can be found at the corresponding section of the
Installation & Administration Guide for the [GCN](gcn/docs/installationguide.md) and the [ICN](icn/docs/installationguide.md).

Example `Dockerfiles` are also provided for each component.

## Usage

The following `docker-compose` can be used to ramp-up and run the stack with all necessary components. However, this is only an example and it is up to the user to properly configure all the services and guarantee the solution security.

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

  # ICN
  icn:
    image: icn
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
```

More detailed information about how to use the FIREFIT ROSE-AP components can be found in the User & Programmers Manual for the [GCN](gcn/docs/usermanual.md) and [ICN](icn/docs/usermanual.md).

## API

Information about the API of the FIREFIT ROSE-AP components can be found in the API documentation for the [GCN](gcn/docs/api.md) and [ICN](icn/docs/api.md).

## License

The FIREFIT ROSE-AP components are licensed under [Affero General Public License (AGPL) version 3](LICENSE).

© 2021 Introsys, S.A.
