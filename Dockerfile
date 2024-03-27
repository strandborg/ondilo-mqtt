#
# Example cmdline for first run:
# docker run -it -e TZ=Europe/Helsinki -e MQTT_BROKER_HOST=XXXX -e MQTT_BROKER_USER=YYYY -e MQTT_BROKER_PASS=ZZZZ -v /path/to/store/auth/token:/data ondilo-mqtt
# 
# Then, to install as daemon:
# docker run -d --restart unless-stopped -e TZ=Europe/Helsinki -e MQTT_BROKER_HOST=XXXX -e MQTT_BROKER_USER=YYYY -e MQTT_BROKER_PASS=ZZZZ ondilo-mqtt

# Use the official Python image as the base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy your Python script and script file into the container
COPY ondilo_mqtt.py .

# Install the libraries
RUN pip install "paho-mqtt>=1.6.1,<2.0" Homie4 ondilo>=0.4.0 python-dateutil

# Run the Python script with environment variables
CMD ["python", "ondilo_mqtt.py"]
