# GCN - Generic Camera Node

The Generic Camera Node (GCN) is a component that aims to easily integrate any generic camera into a FIWARE solution, abstracting the user from entity, device, database and data persistency configurations.

GCN provides the image capture and camera configuration functionalities, and also ensures the obtained images data persistency to a user-defined database service.

Note that at the current state only MongoDB is considered, but the component was designed to scale to other types of database services in the future.

To achieve this, the user is required to develop the necessary mechanisms using the [Python](https://www.python.org/) programming language. All the necessary structures are provided so that the user only has to *fill the gaps*. All the necessary steps to do so are described in the documentation.

## Contents

- [Getting Started](getting-started.md)
- [Architecture](architecture.md)
- [Installation and Administration Guide](installationguide.md)
- [User Manual](usermanual.md)
- [API](api.md)
