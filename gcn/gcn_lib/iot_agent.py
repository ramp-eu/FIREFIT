import json
import requests
from . import logger


class Iota:
    def __init__(self, configuration):
        self.__configuration = configuration
        self.__resource = '/iot/json'
        self.__entity_type = 'camera'
        self.__protocol = 'json'

    def configure_device(self):
        service_json = self.__build_service()
        self.__send_service_configuration(service_json)

        device_json = self.__build_device()
        self.__send_device_configuration(device_json)

    def __build_service(self):
        body = {
            "services": [
                {
                    "resource": self.__resource,
                    "apikey": self.__configuration.api_key,
                    "type": self.__entity_type
                }
            ]
        }

        service_json = json.dumps(body)

        return service_json

    def __send_service_configuration(self, service_json):
        h = {
            'Content-Type': 'application/json',
            'fiware-service': self.__configuration.service,
            'fiware-servicepath': self.__configuration.service_path
        }
        url = '{0}/iot/services'.format(self.__configuration.iota_endpoint)
        r = requests.post(url, headers=h, data=service_json)
        self.__validate_service_response(r, self.__configuration.api_key)

    def __build_device(self):
        body = {
            "devices": [
                {
                    "device_id": self.__configuration.camera_name,
                    "entity_name": self.__configuration.camera_name,
                    "entity_type": self.__entity_type,
                    "protocol": self.__protocol,
                    "transport": self.__configuration.iota_protocol,
                    "attributes": [
                        {
                            "object_id": "configuration",
                            "name": "configuration",
                            "type": "String"
                        }
                    ],
                    "commands": [
                        {
                            "name": "capture",
                            "type": "command"
                        },
                        {
                            "name": "configure",
                            "type": "command"
                        }
                    ]
                }
            ]
        }

        body_json = json.dumps(body)

        return body_json

    def __send_device_configuration(self, device_json):
        h = {
            'Content-Type': 'application/json',
            'fiware-service': self.__configuration.service,
            'fiware-servicepath': self.__configuration.service_path
        }
        url = '{0}/iot/devices'.format(self.__configuration.iota_endpoint)
        r = requests.post(url, headers=h, data=device_json)
        self.__validate_response(r, self.__configuration.camera_name)

    @staticmethod
    def __validate_response(response, device_id):
        if response.ok:
            logger.info('[IoTA]: Device successfully created with the id {}.'.format(device_id))
        elif response.status_code == 409 or response.status_code == 422:
            logger.info('[IoTA]: A device with the id {} already exists.'.format(device_id))
        else:
            logger.error('[IoTA]: An error may have occurred while '
                         'configuring the device {}'.format(device_id))
            raise Exception('[IoTA]: An error may have occurred while '
                            'configuring the device {}'.format(device_id))

    @staticmethod
    def __validate_service_response(response, api_key):
        if response.ok:
            logger.info('[IoTA]: Service successfully created with the ApiKey {}.'.format(api_key))
        elif response.status_code == 409 or response.status_code == 422:
            logger.info('[IoTA]: A service with the ApiKey {} already exists.'.format(api_key))
        else:
            logger.error('[IoTA]: An error may have occurred while '
                         'configuring the service with the ApiKey {}'.format(api_key))
            raise Exception('[IoTA]: An error may have occurred while '
                            'configuring the service with the ApiKey {}'.format(api_key))
