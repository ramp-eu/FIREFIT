# ICN - Image Classification Node

[![Docker badge](https://img.shields.io/docker/pulls/introsyspt/icn.svg)](https://hub.docker.com/repository/docker/introsyspt/icn)

The Image Classification Node (ICN) provides a mechanism to easily integrate Machine Learning or Deep Learning models into a [FIWARE](https://fiware-tutorials.readthedocs.io/en/latest/) solution, with the objective of performing image classification tasks and abstracting the user fom entity, device, database and data persistency configurations.

## Contents

- [Background](#background)
- [Getting Started](#getting-started)
- [Install](#install)
- [Usage](#usage)
- [License](#license)

## Background

ICN provides the image classification and model selection functionalities, and is also able to perform the classification task automatically by subscribing to [Image Reference Entity](../../gcn/data_models/image_reference.json) changes. Although it can be used as an independent component, its full functionality can be achieved when working together with the [Generic Camera Node (GCN)](../../gcn). For this reason, it is advised to consult the [GCN documentation](../../gcn/docs/index.md) before using the ICN.

The ICN can be adapted for custom applications. To achieve this, the user is required to develop the necessary mechanisms using the [Python](https://www.python.org/) programming language. All the necessary structures are provided so that the user only has to *fill the gaps*. All the necessary steps to do so are described in the [documentation](docs/index.md).

Note that, currently, only [MongoDB](https://www.mongodb.com/) is supported for data persistance.

## Getting started

The [step-by-step tutorial](docs/getting-started.md) provides an overall understanding of the component by experimenting simple usage example.

## Install

Information about how to install the ICN can be found at the corresponding section of the
[Installation & Administration Guide](docs/installationguide.md).

## Usage

Detailed information about how to use the ICN can be found in the [User & Programmers Manual](docs/usermanual.md).

## License

The ICN is licensed under [Affero General Public License (AGPL) version 3](../LICENSE).

© 2021 Introsys, S.A.
