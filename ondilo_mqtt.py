import os
import time
import json
from pathlib import Path
from datetime import datetime, timedelta, timezone
from ondilo import Ondilo
from dateutil import parser
from homie.device_base import Device_Base
from homie.node.node_base import Node_Base

from homie.node.property.property_temperature import Property_Temperature
from homie.node.property.property_float import Property_Float

# Get MQTT broker configuration from environment variables

mqtt_settings = {
    'MQTT_BROKER' : os.environ.get("MQTT_BROKER_HOST", "localhost"),
    'MQTT_PORT' : int(os.environ.get("MQTT_BROKER_PORT", 1883)),
    'MQTT_USERNAME' : os.environ.get("MQTT_BROKER_USER", None),
    'MQTT_PASSWORD' : os.environ.get("MQTT_BROKER_PASS", None)
}

device_id = os.environ.get("MQTT_DEVICE_ID", "icopool")
device_name = os.environ.get("MQTT_DEVICE_NAME", "Ondilo ICO Pool")
tokenFile = os.environ.get("OAUTH2_TOKEN_FILE", "/data/ico_token.json")

mqtt_publish_interval = os.environ.get("MQTT_PUBLISH_INTERVAL", 600)

def get_ico_measurements():
    tokenPath = Path(tokenFile)

    if(tokenPath.is_file()):
        client = Ondilo(json.loads(tokenPath.read_text()))
    else:
        client = Ondilo(redirect_uri="https://example.com/api")

        print('Please go here and authorize,', client.get_authurl())

        redirect_response = input('Paste the full redirect URL here:')
        token = client.request_token(authorization_response=redirect_response)

        with open(tokenFile, 'w') as outfile:
            json.dump(token, outfile)

#    print("Found all those pools: ", client.get_pools())

    poolid = client.get_pools()[0]["id"]
    measures = client.get_last_pool_measures(poolid)
    return {item['data_type']: item for item in measures}

class ICO_Device(Device_Base):
    def __init__(
        self,
        device_id=None,
        name=None,
        homie_settings=None,
        mqtt_settings=None,
    ):

        super().__init__(device_id, name, homie_settings, mqtt_settings)

        node = Node_Base(self, "status", "Status", "status")
        self.node = node
        self.add_node(node)

        self.temp = Property_Temperature(self.node, id="temperature", name="Water Temperature", unit="°C")
        self.temp.valueTime = datetime.now(timezone.utc) - timedelta(days=365)
        self.node.add_property(self.temp)
        self.orp = Property_Float(self.node, id="orp", name="ORP", unit="mW", settable=False)
        self.orp.valueTime = datetime.now(timezone.utc) - timedelta(days=365)
        self.node.add_property(self.orp)
        self.ph = Property_Float(self.node, id="ph", name="pH", unit=None, settable=False)
        self.ph.valueTime = datetime.now(timezone.utc) - timedelta(days=365)
        self.node.add_property(self.ph)
        self.salt = Property_Float(self.node, id="salt", name="Salt", unit="mg/l", settable=False)
        self.salt.valueTime = datetime.now(timezone.utc) - timedelta(days=365)
        self.node.add_property(self.salt)

        self.start()    

    def update_prop(self, data, prop):
        if(data["is_valid"]):
            valueTime = parser.parse(data["value_time"])
            if(prop.valueTime < valueTime.astimezone(timezone.utc)):
                prop.value = data["value"]
                prop.valueTime = valueTime

    def update(self):
        measures = get_ico_measurements()
        self.update_prop(measures["temperature"], self.temp)
        self.update_prop(measures["orp"], self.orp)
        self.update_prop(measures["ph"], self.ph)
        self.update_prop(measures["salt"], self.salt)


def main():

    ico = ICO_Device(name=device_name, device_id=device_id, mqtt_settings=mqtt_settings)

    while True:
        ico.update()
        time.sleep(mqtt_publish_interval)

if __name__ == "__main__":
    main()
