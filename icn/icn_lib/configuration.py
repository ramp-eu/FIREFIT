import json
import os
from . import logger


class Configuration:
    def __init__(self):
        self.cb_endpoint = ''
        self.cygnus_endpoint = ''
        self.iota_endpoint = ''
        self.iota_protocol = ''
        self.protocol_broker_address = ''
        self.protocol_broker_port = ''
        self.entity_id = ''
        self.image_entity_id = ''
        self.classifier_id = ''
        self.api_key = ''
        self.service = ''
        self.service_path = ''
        self.host_ip = ''
        self.host_port = ''
        self.model_db_type = ''
        self.model_db_endpoint = ''

        #for the future
        #self.standalone = '' #to work as standalone and ignore iota and orion

    def import_configuration(self, path):
        file_path = os.path.join(path, 'configuration.json')
        data = ''
        with open(file_path, 'r') as f:
            data = json.load(f)
        self.__parse_configuration(data)

    def __parse_configuration(self, data):
        self.cb_endpoint = self.__parse_property(data, 'cb_endpoint')
        self.cygnus_endpoint = self.__parse_property(data, 'cygnus_endpoint')
        self.iota_endpoint = self.__parse_property(data, 'iota_endpoint')
        self.iota_protocol = self.__parse_property(data, 'iota_protocol', mandatory=False, default='MQTT')
        self.protocol_broker_address = self.__parse_property(data, 'protocol_broker_address')
        self.protocol_broker_port = self.__parse_property(data, 'protocol_broker_port')
        self.entity_id = self.__parse_property(data, 'entity_id')
        self.image_entity_id = self.__parse_property(data, 'image_entity_id')
        self.classifier_id = self.__parse_property(data, 'classifier_id')
        self.api_key = self.__parse_property(data, 'api_key')
        self.service = self.__parse_property(data, 'service')

        sp = self.__parse_property(data, 'service_path')
        if sp[0] != '/':
            sp = '/{}'.format(sp)
        self.service_path = sp

        self.host_ip = self.__parse_property(data, 'host_ip')
        self.host_port = self.__parse_property(data, 'host_port')
        self.model_db_type = self.__parse_property(data, 'model_db_type', mandatory=False, default='mongo')
        self.model_db_endpoint = self.__parse_property(data, 'model_db_endpoint')

    def __validate_configuration(self):
        # not used at the moment
        pass

    def __str__(self):
        items = ['{}: {}'.format(item, str(self.__getattribute__(item))) for item in vars(self)]
        output = '\n'.join(items)
        return output

    @staticmethod
    def __parse_property(dict_properties, property_name, mandatory=True, default=None):
        try:
            return dict_properties[property_name]
        except KeyError:
            if mandatory:
                logger.error('[Configuration]: The {} property does not exist in the configuration file, or the '
                             'configuration file does not respect the expected structure.')
                raise Exception('[Configuration]: The {} property does not exist in the configuration file, or the '
                                'configuration file does not respect the expected structure.')
            return default


