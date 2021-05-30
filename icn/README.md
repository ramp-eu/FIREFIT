# ICN - Image Classification Node

[![Docker badge](https://img.shields.io/docker/pulls/introsyspt/icn.svg)](https://hub.docker.com/repository/docker/introsyspt/icn)

The Image Classification Node (ICN) is a component that aims to easily integrate Machine Learning or Deep Learning models to perform image classification tasks into a [FIWARE](https://fiware-tutorials.readthedocs.io/en/latest/) solution, abstracting the user fom entity, device, database and data persistency configurations.

## Contents

- [Background](#background)
- [Install](#install)
- [Usage](#usage)
- [API](#api)
- [License](#license)

## Background

ICN provides the image classification and model selection functionalities, and is also able to perform the classification task automatically by subscribing to [Image Reference Entity](../../gcn/data_models/image_reference.json) changes.

Note that at the current state only [MongoDB](https://www.mongodb.com/) is considered, but the component was designed to scale to other types of database services in the future.

To achieve such functionality, the user is required to develop the necessary mechanisms using the [Python](https://www.python.org/) programming language. All the necessary structures are provided so that the user only has to *fill the gaps*. All the necessary steps to do so are described in the [documentation](docs).

## Install

Information about how to install the ICN can be found at the corresponding section of the
[Installation & Administration Guide](docs/installationguide.md).

## Usage

Detailed information about how to use the ICN can be found in the [User & Programmers Manual](docs/usermanual.md).

## License

The ICN is licensed under [Affero General Public License (AGPL) version 3](../LICENSE).

© 2021 Introsys, S.A.
