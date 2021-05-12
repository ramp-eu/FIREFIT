import json
from icn_api import app_config
from icn_api import schema
from icn_api import ProtoClient
from icn_api import orion
from flask import Flask, request
from marshmallow import ValidationError


app = Flask(__name__)
proto_client = ProtoClient(app_config, app.logger)
proto_client.start()


@app.route('/{}/{}'.format(app_config.api_key, app_config.classifier_id), methods=["POST"])
def post_image_result():
    body = request.json
    app.logger.info(json.dumps(body))
    try:
        schema.load(body)
        try:
            # Update device status
            orion.update_device_command_status('classify', 'PENDING')

            # Extract image reference from subscription
            img_ref = extract_image_reference(body)
            img_ref_json = json.dumps(img_ref)

            # Send command to device
            proto_client.send_command('classify', img_ref_json)
        except Exception as e:
            app.logger.warning(e)
    except ValidationError as e:
        app.logger.error(e)
        return "Unexpected schema received.", 400
    return 'success'


def extract_image_reference(body):
    return body['data'][0]['image']['value']


if __name__ == '__main__':
    # DEVELOPMENT SERVER
    import logging
    from icn_api import orion
    orion.purge_subscriptions()
    orion.configure_entity_sub()

    app.logger.setLevel(logging.DEBUG)

    app.run(host='0.0.0.0', port=int(app_config.host_port), debug=False)
else:
    pass

