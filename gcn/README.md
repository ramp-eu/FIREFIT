# GCN - Generic Camera Node

[![Docker badge](https://img.shields.io/docker/pulls/introsyspt/gcn.svg)](https://hub.docker.com/repository/docker/introsyspt/gcn)

The Generic Camera Node (GCN) is a component that aims to easily integrate any generic camera into a [FIWARE](https://fiware-tutorials.readthedocs.io/en/latest/) solution, abstracting the user from entity, device, database and data persistency configurations.

## Contents

- [Background](#background)
- [Install](#install)
- [Usage](#usage)
- [API](#api)
- [License](#license)

## Background

GCN provides the image capture and camera configuration functionalities, and also ensures the obtained images data persistency to a user-defined database service.

In short terms, the GCN performs the following tasks:

- creates an [Image Reference Entity](data_models/image_reference.json) directly at Orion and the corresponding data persistence at MongoDB through Cygnus,
- creates a representation of the camera as a device at Orion through the IoT Agent with configuration and actuation available,
- creates a database instance at MongoDB to store the obtained images,
- updates the [Image Reference Entity](data_models/image_reference.json) registered at Orion with a new image reference each time the camera captures and stores a new image.

This results in a device entity becoming available at Orion and to which the user can send configuration and capture commands. At each capture, the obtained image is automatically stored at the database and the [Image Reference Entity](data_models/image_reference.json) is updated with the corresponding information. At each configuration command, the processes defined by the user are performed and the device context is also updated at Orion.

Note that at the current state only [MongoDB](https://www.mongodb.com/) is considered, but the component was designed to scale to other types of database services in the future.

To achieve this, the user is required to develop the necessary mechanisms using the [Python](https://www.python.org/) programming language. All the necessary structures are provided so that the user only has to *fill the gaps*. All the necessary steps to do so are described in the [documentation](docs/index.md).

## Install

Information about how to install the GCN can be found at the corresponding section of the
[Installation & Administration Guide](docs/installationguide.md).

## Usage

Detailed information about how to use the GCN can be found in the [User & Programmers Manual](docs/usermanual.md).

## License

The GCN is licensed under [Affero General Public License (AGPL) version 3](../LICENSE).

© 2021 Introsys, S.A.
