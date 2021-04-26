# FIREFIT ROSE-AP

[![License: MIT](https://img.shields.io/github/license/ramp-eu/TTE.project1.svg)](https://opensource.org/licenses/MIT)
[![Docker badge](https://img.shields.io/docker/pulls/ramp-eu/TTE.project1.svg)](https://hub.docker.com/repository/docker/magnoguedes/firefit-rose-ap)
[![Documentation Status](https://readthedocs.org/projects/firefitrose-ap/badge/?version=latest)](https://firefitrose-ap.readthedocs.io/en/latest/?badge=latest)
[![CII Best Practices](https://bestpractices.coreinfrastructure.org/projects/4832/badge)](https://bestpractices.coreinfrastructure.org/projects/4832)

The present repository holds the FIREFIT ROSE-AP components proposed by [Introsys](https://www.introsys.eu/?lang=en) which aim to easily integrate generic cameras and image classification processes into a [FIWARE](https://www.fiware.org/) solution, abstracting the user from concerns such as entity configuration, data persistency, device configuration or database configuration.

This project is part of [DIH^2](http://www.dih-squared.eu/). For more information check the RAMP Catalogue entry for the
[components](https://github.com/xxx).

| :books: [Documentation](https://firefitrose-ap.readthedocs.io/en/latest/) | :whale: [Docker Hub](https://hub.docker.com/repository/docker/magnoguedes/firefit-rose-ap) |
| --------------------------------------------- | ------------------------------------------------------------- |

## Contents

  - [Background](#background)
  - [Install](#install)
  - [Usage](#usage)
  - [API](#api)
  - [Testing](#testing)
  - [License](#license)

## Background

This ROSE-AP solution comprises two main components. The first component, responsible for the cameras integration is the Generic Camera Node (GCN). The second component, responsible for the image classification is the Image Classification Node (ICN).

Due to their synergy, it is possible to consider that any solution implementing the components herein presented is making use of a Vision-based Inspection System. Although this classification depends on the application, it is relevant in the context where ROSE-AP stands, since it was designed as an answer to requirements and optimizations imposed and identified by the [FIREFIT experiment](http://www.dih-squared.eu/TTE-FIREFIT).

The flexibility offered by these components relies heavily in the usage of [Python](https://www.python.org/), an increasingly popular programming language commonly used in Machine Learning and Deep Leaning contexts and hardware communication.

### Introsys
[Introsys](https://www.introsys.eu/?lang=en) is a technology provider and system integrator company dedicated on the creation of customised solution for automation and control systems. Established in 2002 as a spin off from the Electrical Engineering Department of Universidade Nova de Lisboa. It started with 4 employees and as grown to 157 employees with a turnover of 17.500 m€ in 2017. From the 157 employees 70 are graduated engineers and 20 are MSc. From 2004 till now the company has established itself in the market as one of the reference Controls Houses for the European Manufacturing Industry.

The industrial automation department of the company is mainly involved with the development of real time automation solutions for the automotive industry. This department has developed solutions for different companies such as Ford, VW Group, including AUDI and, BMW. These solutions include, hard-ware planning and design, the development of systems control with industrial PLCs as well as robot programming, and robot and PLC process simulation. It has also participated in the development of control specifications for Ford and VW. Currently this department is essentially a provider of high-tech software solutions for automation in the highly competitive European automotive market. It has received several prizes from their customers for highly innovative solutions. As of 2020, Introsys integrated more than 3000 industrial robots in actual production facilities.

Along with the industrial activity, Introsys maintains a Research and Development department dedicated to the development of service mobile robots (co-financed by Portuguese Defence Department, QREN and Portugal2020), advanced manufacturing control systems (co-financed by the European Commission under the Marie Curie program, FP7 and H2020), Non-Destructive Systems for quality inspection, Machine Learning and other solutions, with high focus on vision-based systems, HMI and HRC. The Research and Development is considered an integral part of INTROSYS business in order to keep the company at its most competitive level. In 2017 INTROSYS won two Innovation Prizes and the Born from Knowledge Award.

In 2015-16, Introsys developed a project backed by FIWARE technology – 15443 FRESH experiment for the SmartAgrifood2 project. This promoted a first contact on the team with the platform, the lab and the GE’s, where a Python application was developed to gather and process data from a wireless sensor network deployed in hydroponic greenhouses. Also, in 2015, INTROSYS started four year European project for the factories of the future (openMOS) where it led a 16 partner consortium. Significant contributions to flexible production, plug-and-produce paradigm and skill-based execution concepts were achieved.

### FIWARE
> *[FIWARE](https://www.fiware.org/) is a curated framework of open source platform components which can be assembled together and with other third-party platform components to accelerate the development of Smart Solutions.*

### Dependencies
The GCN and ICN were designed to be integrated into [FIWARE](https://www.fiware.org/) solutions. For this reason, there are several dependencies to Fiware components as well as to third party components widely used throughout the Fiware catalogue.

Although these elements will be presented with more detail in following points, a short list is presented with all the Rose-AP dependencies:
- Fiware
  - [Orion Context Broker](#orion-context-broker)
  - [JSON IoT Agent](#json-iot-agent)
  - [Cygnus](#cygnus)
- Third-party
  - [MongoDB](#mongo-db)
  - [Mosquitto](#mosquitto)

>***It is important for one to be familiar with the Fiware ecosystem and the listed dependencies, despite the information provided through this repository.***

#### Orion Context Broker
*The main and only mandatory component of any “Powered by FIWARE” platform or solution is a FIWARE Context Broker Generic Enabler, bringing a cornerstone function in any smart solution: the need to manage context information, enabling to perform updates and bring access to context.*

In short terms, [Orion Context Broker](https://fiware-orion.readthedocs.io/en/master/) allows to manage information by making use of entities that can be seen as objects in the context of object oriented programming. It manages all the changes regarding those entities and allows the broadcast of those changes to all the other components that are connected to Orion. There are a set of features that Orion makes available like the Publish/Subscribe or the registration of context providers to allow queries of information by demand.

The documentation provided by FIWARE regarding [Orion Context Broker](https://fiware-orion.readthedocs.io/en/master/) is abundant and comprehensive, therefore it would not make sense to present replicated information here.

#### JSON IoT Agent
*An Internet of Things Agent for a JSON based protocol (with AMQP, HTTP and MQTT transports). This IoT Agent is designed to be a bridge between JSON and the NGSI interface of a context broker.*

The [JSON IoT Agent](https://fiware-iotagent-json.readthedocs.io/en/latest/) is an interface that facilitates the integration of IoT devices with all its characteristics in the [Orion Context Broker](#211-orion-context-broker). Additionally, it behaves as a converter between distinct communication protocols that Orion does not understand to HTTP requests understandable by Orion.

The documentation provided by FIWARE regarding the [JSON IoT Agent](https://fiware-iotagent-json.readthedocs.io/en/latest/) is abundant and comprehensive, therefore it would not make sense to present replicated information here.

#### Cygnus
*Cygnus is a connector in charge of persisting context data sources into other third-party databases and storage systems, creating a historical view of the context.*

[Cygnus](https://fiware-cygnus.readthedocs.io/en/latest/https://fiware-cygnus.readthedocs.io/en/latest/) will take care of interpreting the [NGSI v2](https://fiware.github.io/specifications/ngsiv2/stable/) specification used by [Orion](#orion-context-broker) and storing the context changes in each entity that is configured to be watched by Cygnus.

The documentation provided by FIWARE regarding [Cygnus](https://fiware-cygnus.readthedocs.io/en/latest/https://fiware-cygnus.readthedocs.io/en/latest/) is abundant and comprehensive, therefore it would not make sense to present replicated information here.

#### Mongo DB
[MongoDB](https://www.mongodb.com/) is a database that is widely compatible with the [FIWARE components](#21-fiware).

#### Mosquitto
The [Mosquitto](https://mosquitto.org/) is an MQTT broker that allows all the components to communicate via MQTT messages by using a publish/subscribe model.

## Install

Information about how to install the GCN and ICN can be found at the corresponding section of the
[Installation & Administration Guide](docs/installationguide.md).

A `Dockerfile` is also available for your use - further information can be found [here](docker/README.md)

## Usage

Information about how to use the GCN and ICN can be found in the [User & Programmers Manual](docs/usermanual.md).

## API

Information about the API of the GCN and ICN can be found in the [API documentation](docs/api.md).

## Testing

tdb

## License

[MIT](LICENSE) © <TTE>
