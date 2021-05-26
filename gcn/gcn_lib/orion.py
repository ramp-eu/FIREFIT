import json
import requests
from . import logger


class Orion:
    def __init__(self, configuration):
        self.__configuration = configuration
        self.__entity_type = 'imageReference'
        self.__attribute_name = 'image'
        self.__attribute_type = 'reference'
        self.__sub_endpoint = '{}/notify'.format(self.__configuration.cygnus_endpoint)

    # Entity Creation

    def configure_entity(self):
        entity = self.__build_image_result_entity()
        self.__configure_entity(entity)

    def __configure_entity(self, entity_json):
        h = {'Content-Type': 'application/json'}
        url = '{0}/v2/entities'.format(self.__configuration.cb_endpoint)
        r = requests.post(url, headers=h, data=entity_json)
        self.__validate_response(r, self.__configuration.entity_id)

    @staticmethod
    def __validate_response(response, entity_id):
        if response.ok:
            logger.info('[Orion]: Entity successfully created with the id {}.'.format(entity_id))
        elif response.status_code == 409 or response.status_code == 422:
            logger.info('[Orion]: An entity with the id {} already exists.'.format(entity_id))
        else:
            logger.error('[Orion]: An error may have occurred while '
                         'configuring the entity {}'.format(entity_id))
            raise Exception('[Orion]: An error may have occurred while '
                            'configuring the entity {}'.format(entity_id))

    def __build_image_result_entity(self):
        entity = {'id': self.__configuration.entity_id,
                  'type': self.__entity_type,
                  self.__attribute_name: {
                      'type': self.__attribute_type,
                      'value': {
                          'databaseType': self.__configuration.sink,
                          'databaseEndpoint': self.__configuration.sink_endpoint,
                          'database': self.__configuration.service,
                          'collection': self.__configuration.service_path,
                          'imageFile': ''
                      }
                  }}
        entity_json = json.dumps(entity)
        return entity_json

    # Entity update

    def update_image_entity(self, image_file_name):
        h = {'Content-Type': 'application/json'}
        url = '{0}/v2/entities/{1}/attrs/{2}/value'.format(self.__configuration.cb_endpoint,
                                                           self.__configuration.entity_id,
                                                           self.__attribute_name)
        body = {
            'databaseType': self.__configuration.sink,
            'databaseEndpoint': self.__configuration.sink_endpoint,
            'database': self.__configuration.service,
            'collection': self.__configuration.service_path,
            'imageFile': image_file_name
        }

        body_json = json.dumps(body)

        r = requests.put(url, headers=h, data=body_json)

        if r.ok:
            logger.info('[Orion] Image result entity updated.')
            return True

        logger.debug(r.text)
        logger.warning('[Orion] Image result entity update failed.')
        return False

    # Data Persistence

    def configure_entity_data_pers(self):
        if not self.__data_pers_existence(self.__configuration.entity_id):
            self.__data_pers_create('Image Reference data persistence subscription.')

    def __data_pers_existence(self, entity_id):
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
        cond_two = self.__sub_endpoint == sub['notification']['http']['url']
        if cond_one and cond_two:
            logger.info('[Orion]: Subscription for the entity {} already exists. '
                        'Subscription not created.'.format(entity_id))
            return True
        return False

    def __data_pers_create(self, description):
        h = {'Content-Type': 'application/json'}
        url = '{0}/v2/subscriptions'.format(self.__configuration.cb_endpoint)
        payload = self.__data_pers_create_request(description)
        r = requests.post(url, headers=h, data=payload)
        self.__validate_sub_response(r, self.__configuration.entity_id)

    def __data_pers_create_request(self, description):
        pers_req_body = {
            'description': description,
            'subject': {
                'entities': [
                    {
                        'id': self.__configuration.entity_id,
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
                    'url': self.__sub_endpoint
                }
            }
        }

        pers_req_body_json = json.dumps(pers_req_body)

        return pers_req_body_json

    @staticmethod
    def __validate_sub_response(response, entity_id):
        if response.ok:
            logger.info('[Orion]: The entity {} now has data persistence configured.'.format(entity_id))
        else:
            logger.error('[Orion]: Data persistence configuration '
                         'for the entity {} failed.'.format(entity_id))
            raise Exception('[Orion]: Data persistence configuration '
                            'for the entity {} failed.'.format(entity_id))

    # Subscriptions management
    # Orion does not manage subscriptions automatically
    # for that reason, we need to purge subscriptions so that
    # they do not replicate indefinitely

    def purge_subscriptions(self):
        subs = self.__get_subs()
        purge_list = []
        for sub in subs:
            if sub['notification']['http']['url'] == self.__sub_endpoint:
                for ent in sub['subject']['entities']:
                    if self.__configuration.entity_id == ent['id']:
                        purge_list.append(sub['id'])
        for target in purge_list:
            url = '{}/v2/subscriptions/{}'.format(self.__configuration.cb_endpoint, target)
            r = requests.delete(url)
            if r.ok:
                logger.info('[Orion]: Subscription purged ({}).'.format(target))
            else:
                logger.warning('[Orion]: There was a problem in the purge process.')

