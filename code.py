print("Hello World!")
print("Hello World! 2")
import board
import digitalio
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

import wifi
networks = []
g = []
myssid = ""
mypass = ""
broker = '192.168.0.54'
mqttport = 1883
mqttuser = 'admin'
mqttpass = 'admin'

print(dir("/"))
help("modules")

for network in wifi.radio.start_scanning_networks():
    networks.append(network)
wifi.radio.stop_scanning_networks()
networks = sorted(networks, key=lambda net: net.rssi, reverse=True)
for network in networks:
    print("ssid:",network.ssid, "rssi:",network.rssi)
    for secret in secrets:
        print(secrets[secret]['ssid'])
        if network.ssid == secrets[secret]['ssid']:
            myssid = secrets[secret]['ssid']
            mypass = secrets[secret]['password']
            broker = secrets[secret]['broker']
            mqttport = secrets[secret]['port']
            mqttuser = secrets[secret]['user']
            mqttpass = secrets[secret]['pass']

wifi.radio.connect(ssid=myssid,password=mypass)
print("my IP addr:", wifi.radio.ipv4_address)


import ssl
import socketpool
import adafruit_minimqtt.adafruit_minimqtt as MQTT # type: ignore

readableMACaddress = ''.join(['%02X' % i for i in wifi.radio.mac_address])
print("MAC Address:", readableMACaddress)

### Topic Setup ###

# MQTT Topic
# Use this topic if you'd like to connect to a standard MQTT broker
mqtt_topic = "test/topic"

# Adafruit IO-style Topic
# Use this topic if you'd like to connect to io.adafruit.com
# mqtt_topic = secrets["aio_username"] + '/feeds/temperature'

### Code ###
# Define callback methods which are called when events occur
# pylint: disable=unused-argument, redefined-outer-name
def connect(mqtt_client, userdata, flags, rc):
    # This function will be called when the mqtt_client is connected
    # successfully to the broker.
    print("Connected to MQTT Broker!")
    print("Flags: {0}\n RC: {1}".format(flags, rc))


def disconnect(mqtt_client, userdata, rc):
    # This method is called when the mqtt_client disconnects
    # from the broker.
    print("Disconnected from MQTT Broker!")


def subscribe(mqtt_client, userdata, topic, granted_qos):
    # This method is called when the mqtt_client subscribes to a new feed.
    print("Subscribed to {0} with QOS level {1}".format(topic, granted_qos))


def unsubscribe(mqtt_client, userdata, topic, pid):
    # This method is called when the mqtt_client unsubscribes from a feed.
    print("Unsubscribed from {0} with PID {1}".format(topic, pid))


def publish(mqtt_client, userdata, topic, pid):
    # This method is called when the mqtt_client publishes data to a feed.
    print("Published to {0} with PID {1}".format(topic, pid))


def message(client, topic, message):
    # Method called when a client's subscribed feed has a new value.
    print("New message on topic {0}: {1}".format(topic, message))


# Create a socket pool
pool = socketpool.SocketPool(wifi.radio)

# Set up a MiniMQTT Client
mqtt_client = MQTT.MQTT(
    broker=broker,
    port=mqttport,
    username=mqttuser,
    password=mqttpass,
    socket_pool=pool,
    ssl_context=ssl.create_default_context(),
)

# Connect callback handlers to mqtt_client
mqtt_client.on_connect = connect
mqtt_client.on_disconnect = disconnect
mqtt_client.on_subscribe = subscribe
mqtt_client.on_unsubscribe = unsubscribe
mqtt_client.on_publish = publish
mqtt_client.on_message = message

print("Attempting to connect to %s" % mqtt_client.broker)
mqtt_client.connect()

print("Subscribing to %s" % mqtt_topic)
mqtt_client.subscribe(mqtt_topic)

print("Publishing to %s" % mqtt_topic)
mqtt_client.publish(mqtt_topic, "Hello Broker!")

print("Unsubscribing from %s" % mqtt_topic)
mqtt_client.unsubscribe(mqtt_topic)

# print("Disconnecting from %s" % mqtt_client.broker)
# mqtt_client.disconnect()



print(board.SCL)
print(board.SDA)

# while True:
#     print("sleep")
#     time.sleep(100.0)

import time

# List of potential I2C busses
ALL_I2C = ("board.I2C()", "board.STEMMA_I2C()")

# Determine which busses are valid
found_i2c = []
for name in ALL_I2C:
    try:
        print("Checking {}...".format(name), end="")
        bus = eval(name)
        bus.unlock()
        found_i2c.append((name, bus))
        print("ADDED.")
    except Exception as e:
        print("SKIPPED:", e)

# Scan valid busses
if len(found_i2c):
    print("-" * 40)
    print("I2C SCAN")
    print("-" * 40)
    for bus_info in found_i2c:
        name = bus_info[0]
        bus = bus_info[1]

        while not bus.try_lock():
            pass

        print(
            name,
            "addresses found:",
            [hex(device_address) for device_address in bus.scan()],
        )

        bus.unlock()

    time.sleep(2)
else:
    print("No valid I2C bus found.")


# import Adafruit_CircuitPython_TCS34725.adafruit_tcs34725 as TCS
import adafruit_tcs34725

# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
# sensor = TCS.TCS34725(i2c)
sensor = adafruit_tcs34725.TCS34725(i2c)


# Change sensor integration time to values between 2.4 and 614.4 milliseconds
# sensor.integration_time = 150

# Change sensor gain to 1, 4, 16, or 60
# sensor.gain = 4
while True:
    print("sleep")
    time.sleep(100.0)

# Main loop reading color and printing it every second.
while True:
    # Raw data from the sensor in a 4-tuple of red, green, blue, clear light component values
    # print(sensor.color_raw)

    color = sensor.color
    color_rgb = sensor.color_rgb_bytes
    print(
        "RGB color as 8 bits per channel int: #{0:02X} or as 3-tuple: {1}".format(
            color, color_rgb
        )
    )

    # Read the color temperature and lux of the sensor too.
    temp = sensor.color_temperature
    lux = sensor.lux
    print("Temperature: {0}K Lux: {1}\n".format(temp, lux))
    # Delay for a second and repeat.
    time.sleep(1.0)
