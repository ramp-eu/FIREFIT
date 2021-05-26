# FIREFIT ROSE-AP

[![License: AGPL-3.0](https://img.shields.io/github/license/ramp-eu/TTE.project1.svg)](https://opensource.org/licenses/AGPL-3.0)
[![Docker badge](https://img.shields.io/docker/pulls/ramp-eu/TTE.project1.svg)](https://hub.docker.com/repository/docker/magnoguedes/firefit-rose-ap)
[![Documentation Status](https://readthedocs.org/projects/firefitrose-ap/badge/?version=latest)](https://firefitrose-ap.readthedocs.io/en/latest/?badge=latest)
[![CII Best Practices](https://bestpractices.coreinfrastructure.org/projects/4832/badge)](https://bestpractices.coreinfrastructure.org/projects/4832)

The present repository holds the FIREFIT ROSE-AP components proposed by [Introsys](https://www.introsys.eu/?lang=en) which aim to easily integrate generic cameras and image classification processes into a [FIWARE](https://www.fiware.org/) solution, abstracting the user from concerns such as entity configuration, data persistency, device configuration or database configuration.

This project is part of [DIH^2](http://www.dih-squared.eu/). For more information check the RAMP Catalogue entry for the [components](https://github.com/xxx).

| :books: [Documentation](https://firefitrose-ap.readthedocs.io/en/latest/) |:whale: [Docker Hub](https://hub.docker.com/repository/docker/magnoguedes/firefit-rose-ap) | :camera: [GCN](./gcn/) | :mag: [ICN](./icn/)
| --- | --- | --- | --- |

## Contents

- [Background](#background)
- [Install](#install)
- [Usage](#usage)
- [API](#api)
- [License](#license)

## Background

This ROSE-AP solution is composed by two main components:

- The [Generic Camera Node (GCN)](./gcn/) enables simple integration of industrial cameras in the FIWARE ecosystem.
- The [Image Classification Node (ICN)](./icn/) was designed to facilitate the development and integration of image processing algorithms and machine learning tools for feature classification in images.

Due to their synergy, it is possible to consider that any solution implementing the components herein presented is making use of a Vision-based Inspection System. Although this classification depends on the application, it is relevant in the context where ROSE-AP stands, since it was designed as an answer to requirements and optimizations imposed and identified by the [FIREFIT experiment](http://www.dih-squared.eu/TTE-FIREFIT).

The flexibility offered by these components relies heavily in the usage of [Python](https://www.python.org/), an increasingly popular programming language commonly used in Machine Learning and Deep Leaning contexts and hardware communication.

### Introsys

[Introsys](https://www.introsys.eu/?lang=en) is a technology provider and system integrator company dedicated on the creation of customized solutions for automation, control systems and quality inspection.

### FIWARE

[FIWARE](https://www.fiware.org/) is a curated framework of open source platform components which can be assembled together and with other third-party platform components to accelerate the development of Smart Solutions.

## Install

Information about how to install the FIREFIT ROSE-AP components can be found at the corresponding section of the
Installation & Administration Guide for the [GCN](gcn/docs/installationguide.md) and the [ICN](icn/docs/installationguide.md).

Example `docker-compose` files are also provided for each component.

## Usage

Information about how to use the FIREFIT ROSE-AP components can be found in the User & Programmers Manual for the [GCN](gcn/docs/usermanual.md) and [ICN](icn/docs/usermanual.md).

## API

Information about the API of the FIREFIT ROSE-AP components can be found in the API documentation for the [GCN](gcn/docs/api.md) and [ICN](icn/docs/api.md).

## License

The FIREFIT ROSE-AP components are licensed under [Affero General Public License (AGLP) version 3](LICENSE).

© 2021 Introsys, S.A.
