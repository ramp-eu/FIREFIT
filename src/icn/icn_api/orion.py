import json
import requests
from datetime import datetime, timezone
from . import logger


class Orion:
    def __init__(self, configuration):
        self.__configuration = configuration
        self.__entity_type = 'imageReference'
        self.__attribute_name = 'image'
        self.__device_type = 'classifier'
        self.__host_endpoint = "http://{}:{}/{}/{}".format(self.__configuration.host_ip,
                                                           self.__configuration.host_port,
                                                           self.__configuration.api_key,
                                                           self.__configuration.classifier_id)
    # Device entity update

    def update_device_command_status(self, command, status):
        h = {
            'Content-Type': 'application/json',
            'fiware-service': self.__configuration.service,
            'fiware-servicepath': self.__configuration.service_path
        }
        com = "{}_status".format(command)

        url = '{0}/v2/op/update/'.format(self.__configuration.cb_endpoint)

        instant = datetime.now(timezone.utc).isoformat()[:-10] + 'Z'

        body = {
            "actionType": "update",
            "entities": [
                {
                    "id": self.__configuration.classifier_id,
                    "type": self.__device_type,
                    "TimeInstant": {
                        "type": "DateTime",
                        "value": instant
                    },
                    com: {
                        "type": "commandStatus",
                        "value": status,
                        "metadata": {
                            "TimeInstant": {
                                "type": "DateTime",
                                "value": instant
                            }
                        }
                    }
                }
            ]
        }

        body_json = json.dumps(body)

        r = requests.post(url, headers=h, data=body_json)
        if r.ok:
            logger.info('[Orion] Device command status updated.')
            return True
        logger.debug(r.text)
        logger.warning('[Orion] Device command status update failed.')
        return False

    # API subscription

    def configure_entity_sub(self):
        if not self.__sub_existence(self.__configuration.image_entity_id):
            self.__sub_create('ICN API subscription.')

    def __sub_existence(self, entity_id):
        subs = self.__get_subs()
        validation = False
        for sub in subs:
            if self.__is_a_sub(sub, entity_id):
                validation = True
        return validation

    def __get_subs(self):
        url = '{0}/v2/subscriptions'.format(self.__configuration.cb_endpoint)
        r = requests.get(url)
        return json.loads(r.text)

    def __is_a_sub(self, sub, entity_id):
        entities = sub['subject']['entities']

        cond_one = any(entity_id == entity['id'] for entity in entities)
        cond_two = self.__host_endpoint == sub['notification']['http']['url']

        if cond_one and cond_two:
            logger.info('[Orion]: Subscription for ICN API already exists, subscription not created.'.format(entity_id))
            return True
        return False

    def __sub_create(self, description):
        h = {'Content-Type': 'application/json'}
        url = '{0}/v2/subscriptions'.format(self.__configuration.cb_endpoint)
        payload = self.__sub_create_request(description)
        r = requests.post(url, headers=h, data=payload)
        self.__validate_sub_response(r, self.__configuration.image_entity_id)

    def __sub_create_request(self, description):
        pers_req_body = {
            'description': description,
            'subject': {
                'entities': [
                    {
                        'id': self.__configuration.image_entity_id,
                        'type': self.__entity_type
                    }
                ],
                'condition': {
                    'attrs': [
                        self.__attribute_name
                    ]
                }
            },
            'notification': {
                'http': {
                    'url': self.__host_endpoint
                }
            }
        }

        pers_req_body_json = json.dumps(pers_req_body)

        return pers_req_body_json

    @staticmethod
    def __validate_sub_response(response, entity_id):
        if response.ok:
            logger.info('[Orion]: ICN API subscription configured.'.format(entity_id))
        else:
            logger.error('[Orion]: ICN API subscription failed.'.format(entity_id))
            raise Exception('[Orion]: ICN API subscription failed.'.format(entity_id))

    # Subscriptions management
    # Orion does not manage subscriptions automatically
    # for that reason, we need to purge subscriptions so that
    # they do not replicate indefinitely

    def purge_subscriptions(self):
        subs = self.__get_subs()
        purge_list = []
        for sub in subs:
            if sub['notification']['http']['url'] == self.__host_endpoint:
                for ent in sub['subject']['entities']:
                    if self.__configuration.image_entity_id == ent['id']:
                        purge_list.append(sub['id'])
        for target in purge_list:
            url = '{}/v2/subscriptions/{}'.format(self.__configuration.cb_endpoint, target)
            r = requests.delete(url)
            if r.ok:
                logger.info('[Orion]: Subscription purged ({}).'.format(target))
            else:
                logger.warning('[Orion]: There was a problem in the purge process.')





