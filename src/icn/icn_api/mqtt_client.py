import json
import uuid
import base64
import paho.mqtt.client as mqtt


class MqttClient:
    def __init__(self, configuration, logger):
        self.__configuration = configuration
        self.__logger = logger
        self.__client_id = '{}_{}_{}'.format(self.__configuration.api_key,
                                             self.__configuration.classifier_id,
                                             self.generate_uuid())
        self.__mqtt = mqtt.Client(client_id=self.__client_id)
        self.__device_partial_topic = '/{}/{}'.format(self.__configuration.api_key,
                                                      self.__configuration.classifier_id)
        self.__configure_mqtt()

    def __configure_mqtt(self):
        self.__mqtt.on_connect = self.__on_connect_handler
        self.__mqtt.on_disconnect = self.__on_disconnect_handler

    def __on_connect_handler(self, client, userdata, flags, rc):
        self.__logger.info('[MQTT]: Client {} connected to broker.'.format(self.__client_id))

    def __on_disconnect_handler(self, client, userdata, rc):
        self.__logger.warning('[MQTT]: Client {} disconnected from the broker.'.format(self.__client_id))

    def start(self):
        self.__mqtt.connect(self.__configuration.protocol_broker_address,
                            int(self.__configuration.protocol_broker_port))
        self.__mqtt.loop_start()

    def send_command(self, command, content):
        topic = '{}/cmd'.format(self.__device_partial_topic)
        body = {
            command: content
        }
        body_json = json.dumps(body)
        self.__mqtt.publish(topic=topic, payload=body_json, qos=1, retain=False)

    @staticmethod
    def generate_uuid():
        r_uuid = base64.urlsafe_b64encode(uuid.uuid4().bytes)
        return str(r_uuid).replace('=', '')

