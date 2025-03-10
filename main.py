import requests
import time
import paho.mqtt.client as mqtt
from bs4 import BeautifulSoup
import os

# MQTT configuration
MQTT_BROKER = os.environ.get("MQTT_BROKER")  # get mqtt broker adress from environment
MQTT_PORT = int(os.environ.get("MQTT_PORT", 1883))
MQTT_TOPIC_POWER = "solar/power"
MQTT_TOPIC_DAILY_YIELD = "solar/daily_yield"
MQTT_TOPIC_TOTAL_YIELD = "solar/total_yield"
UPDATE_INTERVAL = int(os.environ.get("UPDATE_INTERVAL", 60))

# WebBox URL
WEBBOX_URL = os.environ.get("WEBBOX_URL") + ("/home.htm") # get webbox url from environment

if "//home.htm" in WEBBOX_URL:
    WEBBOX_URL = WEBBOX_URL.replace("//home.htm", "/home.htm")

if WEBBOX_URL.startswith("https://"):
    WEBBOX_URL = "http://" + WEBBOX_URL[8:]
elif not WEBBOX_URL.startswith("http://"):
    WEBBOX_URL = "http://" + WEBBOX_URL

# output config
print("MQTT Broker: " + MQTT_BROKER)
print("MQTT Port: " + str(MQTT_PORT))
print("Webbox Request url: " + WEBBOX_URL)
print("Update Interval: " + str(UPDATE_INTERVAL))

# configure mqtt-client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(MQTT_BROKER, MQTT_PORT, 60)

def fetch_data():
    try:
        response = requests.get(WEBBOX_URL, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # extract values from html, remove unit and replace the "," with a "."

        # POWER
        power = soup.find(id="Power").text.strip().split(" ")[0].replace(",", ".")
        print(power)

        # DAILY_YIELD
        daily_yield_text = soup.find(id="DailyYield").text.strip()
        daily_yield = daily_yield_text.split(" ")[0].replace(",", ".")

        if " Wh" in daily_yield_text: # Make sure the value gets converted to kWh
            daily_yield = float(daily_yield) * (1/1000)
        print(daily_yield)

        # TOTAL YIELD
        total_yield = soup.find(id="TotalYield").text.strip().split(" ")[0].replace(",", ".")
        
        return power, daily_yield, total_yield
    except Exception as e:
        print(f"Fehler beim Abrufen der Daten: {e}")
        return None, None, None

def publish_mqtt(power, daily_yield, total_yield):
    if power and daily_yield and total_yield:
        client.publish(MQTT_TOPIC_POWER, power)
        client.publish(MQTT_TOPIC_DAILY_YIELD, daily_yield)
        client.publish(MQTT_TOPIC_TOTAL_YIELD, total_yield)
        print(f"Gesendet: Leistung={power}, Tagesertrag={daily_yield}, Gesamtertrag={total_yield}")
    else:
        print("Ungültige Daten, MQTT-Übertragung übersprungen.")

if __name__ == "__main__":
    while True:
        power, daily_yield, total_yield = fetch_data()
        publish_mqtt(power, daily_yield, total_yield)
        time.sleep(UPDATE_INTERVAL)
