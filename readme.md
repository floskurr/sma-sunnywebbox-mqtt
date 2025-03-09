# Sunny Webbox to MQTT ☀️📡🔗

A lightweight Docker container/script that retrieves real-time power data from an SMA Sunny Webbox and publishes it via MQTT to the solar/ topic. ⚡📊🚀

## Features ✅📡🌞

- Scrapes **current power**, **daily yield**, and **total yield** from the SMA Sunny Webbox
- Publishes data to an MQTT broker
- Configurable update interval
- all running inside a Docker container

## Installation 🛠️📥🐳

### 1. Clone the Repository 📂💻🔧

```bash
git clone https://github.com/floskurr/sma-sunnywebbox-mqtt.git
cd sma-sunnywebbox-mqtt
```

### 2. Build the Docker Image 🏗️🐳⚙️

```bash
docker build -t sunnywebbox-mqtt .
```

### 3. Run the Container 🚀📡🖥️

Start the container with default settings:

```bash
docker run -d --name sunnywebbox --restart unless-stopped -e MQTT_BROKER="THE_URL_OF_YOUR_MQTT_BROKER" -e WEBBOX_URL="THE_IP_OF_YOUR_SUNNY_WEBBOX" sunnywebbox-mqtt
```

### 4. Custom Configuration ⚙️📡🔧

- **Using a non-default MQTT port:**

    add the following to the docker run command

    ```bash
    -e MQTT_PORT=YOUR_MQTT_PORT
    ```

- **Adjusting the update interval (default: 60 seconds):**

    ```bash
    -e UPDATE_INTERVAL=YOUR_DESIRED_INTERVAL_IN_SECONDS
    ```

## Notes 📌🔍📢

- Ensure your MQTT broker is running and accessible.
- The Webbox URL should be reachable from the container.
- Logs can be checked using:

    ```bash
    docker logs -f sunnywebbox
    ```

## License 📜🔓🌍

This project is open-source under the MIT License.
