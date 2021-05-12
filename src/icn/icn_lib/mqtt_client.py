import json
import time
import threading
import paho.mqtt.client as mqtt
from . import logger


class MqttClient:
    def __init__(self, configuration, classifier_engine):
        self.__configuration = configuration
        self.__classifier = classifier_engine
        self.__th = None
        self.__mqtt = mqtt.Client(client_id='{}_{}'.format(self.__configuration.api_key,
                                                           self.__configuration.classifier_id))
        self.__device_partial_topic = '/{}/{}'.format(self.__configuration.api_key,
                                                      self.__configuration.classifier_id)
        self.__lock = threading.Lock()
        self.__str_classify_cmd = 'classify'
        self.__str_select_model_cmd = 'selectModel'
        self.__str_list_model_cmd = 'listModels'
        self.__str_active_model_attr = 'activeModel'
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
            if self.__str_classify_cmd in packet.keys():
                logger.info('[MQTT]: Classify command received.')

                self.__lock.acquire()
                if not self.__classifier.is_busy:
                    self.__classifier.is_busy = True
                    self.__lock.release()

                    image_reference = packet[self.__str_classify_cmd]
                    image_reference_json = json.loads(image_reference)

                    self.__th = threading.Thread(target=self.__cmd_classify,
                                                 kwargs={'image_reference_dict': image_reference_json})
                    self.__th.start()
                else:
                    self.__lock.release()
                    self.__command_busy_response(self.__str_classify_cmd)
            elif self.__str_select_model_cmd in packet.keys():
                logger.info('[MQTT]: Model selection command received.')

                changed = False

                while not changed:
                    self.__lock.acquire()
                    if not self.__classifier.is_busy:
                        self.__classifier.is_busy = True
                        self.__lock.release()

                        model_name = packet[self.__str_select_model_cmd]

                        self.__th = threading.Thread(target=self.__cmd_select_model,
                                                     kwargs={'model_name': model_name})
                        self.__th.start()
                        changed = True
                    else:
                        time.sleep(0.2)
                        self.__lock.release()

            elif self.__str_list_model_cmd in packet.keys():
                logger.info('[MQTT]: Model listing command received.')

                self.__lock.acquire()

                if not self.__classifier.is_busy:
                    self.__classifier.is_busy = True
                    self.__lock.release()

                    self.__th = threading.Thread(target=self.__cmd_list_models)
                    self.__th.start()
                else:
                    self.__lock.release()
                    self.__command_busy_response(self.__str_list_model_cmd)
        except Exception as e:
            logger.error('[MQTT]: Exception during mqtt message handling. {0}'.format(e))

    def __cmd_classify(self, image_reference_dict):
        result = self.__classifier.classify(image_reference_dict)
        logger.info('[MQTT]: Classification command issued.')
        if result:
            self.__command_response(self.__str_classify_cmd, 'true')
        else:
            self.__command_response(self.__str_classify_cmd, 'false')
        pass

    def __cmd_select_model(self, model_name):
        r = self.__classifier.assign_model(model_name)
        logger.info('[MQTT]: Model selection command issued.')
        if r:
            self.__update_attributes(self.__str_active_model_attr, model_name)
            self.__command_response(self.__str_select_model_cmd, model_name)
        else:
            self.__command_response(self.__str_select_model_cmd, 'false')

    def __cmd_list_models(self):
        models = self.__classifier.list_models()
        logger.info('[MQTT]: Model listing command issued.')
        self.__command_response(self.__str_list_model_cmd, models)

    def __update_attributes(self, attribute, body):
        logger.debug('[MQTT]: Publishing device configuration update.')
        attributes_topic = '{}/attrs'.format(self.__device_partial_topic)
        payload = {
            attribute: body
        }
        payload_json = json.dumps(payload)
        self.__mqtt.publish(topic=attributes_topic, payload=payload_json, qos=2, retain=False)
        logger.debug('[MQTT]: Device configuration update published.')

    def __command_response(self, command, response):
        cmdexe_topic = '{}/cmdexe'.format(self.__device_partial_topic)
        body = {
            command: response
        }
        payload_json = json.dumps(body)
        self.__mqtt.publish(topic=cmdexe_topic, payload=payload_json, qos=2, retain=False)

    def __command_busy_response(self, command):
        cmdexe_topic = '{}/cmdexe'.format(self.__device_partial_topic)
        body = {
            command: "Device is busy, command not executed."
        }
        payload_json = json.dumps(body)
        self.__mqtt.publish(topic=cmdexe_topic, payload=payload_json, qos=1, retain=False)

    def __on_disconnect_handler(self, client, userdata, rc):
        logger.warning('[MQTT]: Disconnected from the broker.')

    def start(self):
        self.__mqtt.connect(self.__configuration.protocol_broker_address,
                            int(self.__configuration.protocol_broker_port))
        self.__mqtt.loop_forever()
