# GCN Architecture

In short terms, GCN will make a configurable camera device available at Orion that allows users to capture images while storing them in a database service.

When GCN starts it communicates via HTTP with Orion, creating the Image Reference Entity and the corresponding data persistency, ensured by Cygnus. Then, it communicates with JSON IoT Agent also via HTTP to create the camera device, which in turn will create the corresponding entity at Orion (IoT Agent intrinsic functionality). From this point on, a camera device with the capture and configure commands is available at Orion, and the intrinsic functionality of generic devices is ensured by the JSON IoT Agent.

At each capture command issued, the GCN will perform the user-defined capture operation and will store the corresponding result at the image database service, updating the Image Reference Entity with the corresponding context data at Orion.

At each configure command issued, the GCN will perform the user-defined camera configuration operation, updating the device attributes at Orion to reflect the current configuration.

To issue these commands one can use HTTP requests or direct MQTT messages, both respecting the FIWARE JSON IoT Agent functionality. For the latter, one needs to be aware that the IoT Agent will not be handling the execution requests (southbound functionality) and therefore will not update the device context data to PENDING status for the corresponding command.

The following image presents how GCN positions itself in a FIWARE solution:

<div>
  <p align="center">
    <img src="gcn.png"/>
  </p>
  <p align="center">Generic Camera Node</p>
</div>

Note that the dependency on a message broker such as Mosquitto (depending on IoT Agent configuration) and on the entity data persistency service Cygnus still exist. In the previous image, these can be considered to be implicitly included into the IoT Agent and Orion respectively.
