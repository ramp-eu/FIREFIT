# ICN - Image Classification Node

The [Image Classification Node (ICN)](../) aims to easily integrate Machine Learning or Deep Learning models to perform **image classification** tasks into a [FIWARE](https://fiware-tutorials.readthedocs.io/en/latest/index.html) solution, abstracting the user fom entity, device, database and data persistency configurations.

[ICN](../) provides the image classification and model selection functionalities, and is also able to perform the classification task automatically by subscribing to [Image Reference Entity](../../gcn/data_models/image_reference.json) changes. Note that at the current state only MongoDB is considered, but the component was designed to scale to other types of database services in the future.

To achieve such functionality, the user is required to develop the necessary mechanisms using the [Python](https://www.python.org/) programming language. All the necessary structures are provided so that the user only has to *fill the gaps*. All the necessary steps to do so are described in the documentation.

## Contents

- [Getting Started](getting-started.md)
- [Architecture](architecture.md)
- [Installation and Administration Guide](installationguide.md)
- [User Manual](usermanual.md)
- [API](api.md)

---

**Next:** [Architecture](architecture.md)
