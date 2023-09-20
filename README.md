# Ondilo-MQTT
 Ondilo ICO - MQTT bridge with Homie 4.0 conventions

This is a simple Docker image with a python script to read in Ondilo ICO readings and send them to MQTT server using Homie 4.0 MQTT conventions. At least OpenHAB is able to auto-discover the items when MQTT Broker is set up correctly.

# Pre-requisites
- Ondilo ICO account set up
- MQTT Server accessible from the docker image
- A folder in the Docker host to store the ICO auth tokens

# Installation and usage

Run the following command to perform the first-time authentication:

```
docker run -it -e TZ=<your timezone> -e MQTT_BROKER_HOST=XXXX -e MQTT_BROKER_USER=YYYY -e MQTT_BROKER_PASS=ZZZZ -v <folder_to_store_the_auth_token>:/data strandborg/ondilo-mqtt:latest
```
The command line will instruct you to visit an URL to log in. Perform login process and copypaste the redirected URL back to the terminal. Press Ctrl-C to quit.

To install the image as a daemon:

```
docker run -d --restart unless-stopped -e TZ=<your timezone> -e MQTT_BROKER_HOST=XXXX -e MQTT_BROKER_USER=YYYY -e MQTT_BROKER_PASS=ZZZZ -v <folder_to_store_the_auth_token>:/data strandborg/ondilo-mqtt:latest
```

# Env variables

```
MQTT_BROKER_HOST - IP address or hostname of the MQTT Server, defaults to localhost
MQTT_BROKER_PORT - IP port of the MQTT Server, defaul 1883
MQTT_BROKER_USER - username to MQTT Server, if it requires authentication
MQTT_BROKER_PASS - password to MQTT Server

MQTT_DEVICE_ID - The device ID that will show up in Homie MQTT topic, defaults to "icopool"
MQTT_DEVICE_NAME - The human-readable device name in Homie MQTT, defaults to "Ondilo ICO Pool"
OAUTH2_TOKEN_FILE - Path (within Docker container) to the auth token file, defaults to /data/ico_token.json
```

