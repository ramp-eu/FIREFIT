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
  - [License](#license)

## Background

This ROSE-AP solution comprises two main components. The first component, responsible for the cameras integration is the Generic Camera Node (GCN). The second component, responsible for the image classification is the Image Classification Node (ICN).

Due to their synergy, it is possible to consider that any solution implementing the components herein presented is making use of a Vision-based Inspection System. Although this classification depends on the application, it is relevant in the context where ROSE-AP stands, since it was designed as an answer to requirements and optimizations imposed and identified by the [FIREFIT experiment](http://www.dih-squared.eu/TTE-FIREFIT).

The flexibility offered by these components relies heavily in the usage of [Python](https://www.python.org/), an increasingly popular programming language commonly used in Machine Learning and Deep Leaning contexts and hardware communication.

#### Introsys
[Introsys](https://www.introsys.eu/?lang=en) is a technology provider and system integrator company dedicated on the creation of customized solutions for automation, control systems and quality inspection.

#### FIWARE
[FIWARE](https://www.fiware.org/) is a curated framework of open source platform components which can be assembled together and with other third-party platform components to accelerate the development of Smart Solutions.


## Install

Information about how to install the GCN and ICN can be found at the corresponding section of the
[Installation & Administration Guide](docs/installationguide.md).

A `Dockerfile` is also available for your use - further information can be found [here](docker/README.md)

## Usage

Information about how to use the GCN and ICN can be found in the [User & Programmers Manual](docs/usermanual.md).

## API

Information about the API of the GCN and ICN can be found in the [API documentation](docs/api.md).

## License

[MIT](LICENSE) © <TTE>
