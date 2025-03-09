# Sunny Webbox to mqtt

A simple docker container / script which scrapes the current power, daily_yield, total_yield from a sma sunny webbox and publishes the data to the solar/ topic via mqtt

## Installation

clone the repo

```bash
git clone https://github.com/floskurr/sma-sunnywebbox-mqtt.git
```

build the docker image

```bash
docker build -t sunnywebbox-mqtt .
```

start the container

```bash
docker run -d --name sunnywebbox --restart unless-stopped -e MQTT_BROKER="THE_URL_OF_YOUR_MQTT_BROKER" -e WEBBOX_URL="THE_IP_OF_YOUR_SUNNY_WEBBOX" sunnywebbox-mqtt
```

or if you are using another port than `1883` for mqtt

```bash
docker run -d --name sunnywebbox --restart unless-stopped -e MQTT_BROKER="THE_URL_OF_YOUR_MQTT_BROKER" -e MQTT_PORT=YOUR_MQTT_PORT -e WEBBOX_URL="THE_IP_OF_YOUR_SUNNY_WEBBOX" sunnywebbox-mqtt
```

if you want to change the default update interval (of 60 seconds) you can set the value (in seconds) as the `UPDATE_INTERVAL` environment variable.
