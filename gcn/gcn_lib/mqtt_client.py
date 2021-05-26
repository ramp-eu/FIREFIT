import json
import threading
import paho.mqtt.client as mqtt
from . import logger


class MqttClient:
    def __init__(self, configuration, camera_engine):
        self.__configuration = configuration
        self.__camera = camera_engine
        self.__th = None
        self.__mqtt = mqtt.Client(client_id='{}_{}'.format(self.__configuration.api_key,
                                                           self.__configuration.camera_name))
        self.__device_partial_topic = '/{}/{}'.format(self.__configuration.api_key,
                                                      self.__configuration.camera_name)
        self.__lock = threading.Lock()
        self.__configure_mqtt()

    def __configure_mqtt(self):
        self.__mqtt.on_connect = self.__on_connect_handler
        self.__mqtt.on_message = self.__on_message_handler
        self.__mqtt.on_disconnect = self.__on_disconnect_handler

    def __on_connect_handler(self, client, userdata, flags, rc):
        logger.info('[MQTT]: Connected to broker.')
        cmd_topic = '{}/cmd'.format(self.__device_partial_topic)
        self.__mqtt.subscribe(cmd_topic)

    def __on_message_handler(self, client, userdata, msg):
        logger.debug('[MQTT]: Message received:\n'
                     'Topic: {0}\nMessage: {1}'.format(msg.topic, msg.payload))
        packet = json.loads(msg.payload)
        try:
            if 'capture' in packet.keys():
                logger.info('[MQTT]: Capture command received.')

                self.__lock.acquire()
                if not self.__camera.is_busy:
                    self.__camera.is_busy = True
                    self.__lock.release()

                    # perform capture operation (camera module)
                    self.__th = threading.Thread(target=self.__capture_command)
                    self.__th.start()
                else:
                    self.__lock.release()
                    self.__command_busy_response('capture')
            elif 'configure' in packet.keys():
                logger.info('[MQTT]: Configuration command received.')

                self.__lock.acquire()
                if not self.__camera.is_busy:
                    self.__camera.is_busy = True
                    self.__lock.release()

                    device_config = packet['configure']

                    # perform configuration operation (camera module)
                    self.__th = threading.Thread(target=self.__configure_command,
                                                 kwargs={'device_config': device_config})
                    self.__th.start()
                else:
                    self.__lock.release()
                    self.__command_busy_response('configure')
        except Exception as e:
            logger.error('[MQTT]: Exception during mqtt message handling. {0}'.format(e))

    def __capture_command(self):
        self.__camera.capture()
        logger.info('[MQTT]: Capture command issued.')
        self.__command_response('capture', 'true')

    def __configure_command(self, device_config):
        self.__camera.configure(device_config)
        logger.info('[MQTT]: Configuration command issued.')
        self.__update_attributes('configuration', device_config)
        self.__command_response('configure', device_config)

    def __update_attributes(self, attribute, body):
        logger.debug('[MQTT]: Publishing device configuration update.')
        attributes_topic = '{}/attrs'.format(self.__device_partial_topic)
        payload = {
            attribute: body
        }
        payload_json = json.dumps(payload)
        self.__mqtt.publish(attributes_topic, payload_json)
        logger.debug('[MQTT]: Device configuration update published.')

    def __command_response(self, command, response):
        cmdexe_topic = '{}/cmdexe'.format(self.__device_partial_topic)
        body = {
            command: response
        }
        payload_json = json.dumps(body)
        self.__mqtt.publish(cmdexe_topic, payload_json)

    def __command_busy_response(self, command):
        cmdexe_topic = '{}/cmdexe'.format(self.__device_partial_topic)
        body = {
            command: "Device is busy, command not executed."
        }
        payload_json = json.dumps(body)
        self.__mqtt.publish(cmdexe_topic, payload_json)

    def __on_disconnect_handler(self, client, userdata, rc):
        logger.warning('[MQTT]: Disconnected from the broker.')

    def start(self):
        self.__mqtt.connect(self.__configuration.protocol_broker_address,
                            int(self.__configuration.protocol_broker_port))
        self.__mqtt.loop_forever()
