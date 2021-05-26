from .mqtt_client import MqttClient


class ProtoClient:
    def __init__(self, configuration, logger):
        self.__config = configuration
        self.__logger = logger
        self.__client = None
        self.__initialize_client()

    def __initialize_client(self):
        if self.__config.iota_protocol == 'MQTT':
            self.__client = MqttClient(self.__config, self.__logger)
        else:
            self.__logger.error("No valid IoT Agent configured, 'MQTT' will be considered")
            self.__client = MqttClient(self.__config, self.__logger)

    def start(self):
        self.__logger.info('Starting the {} client.'.format(self.__config.iota_protocol))
        self.__client.start()

    def send_command(self, command, content):
        self.__logger.info('Sending command to device via {}.'.format(self.__config.iota_protocol))
        self.__client.send_command(command, content)



