import time
import board
import digitalio
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise
import wifi
import ssl
import socketpool

networks = []
# g = []
# myssid = ""
# mypass = ""
# broker = '192.168.0.54'
# mqttport = 1883
# mqttuser = 'admin'
# mqttpass = 'admin'

# print(dir(board))
help("modules")

for network in wifi.radio.start_scanning_networks():
    networks.append(network)
wifi.radio.stop_scanning_networks()
networks = sorted(networks, key=lambda net: net.rssi, reverse=True)
for network in networks:
    # print("ssid:",network.ssid, "rssi:",network.rssi)
    for secret in secrets:
        # print(secrets[secret]['ssid'])
        if network.ssid == secrets[secret]['ssid']:
            myssid = secrets[secret]['ssid']
            mypass = secrets[secret]['password']
            broker = secrets[secret]['broker']
            mqttport = secrets[secret]['port']
            mqttuser = secrets[secret]['user']
            mqttpass = secrets[secret]['pass']

wifi.radio.connect(ssid=myssid,password=mypass)
print("my IP addr:", wifi.radio.ipv4_address)
print("dns:", wifi.radio.ipv4_dns)



pool = socketpool.SocketPool(wifi.radio)

# Get IP address of google.com
try:
    result = pool.getaddrinfo("mqtt.savvyaxl.com.br", 80)
    ip_address = result[0][-1][0]  # Extract IP address
    print(f"IP address of google.com: {ip_address}")
except Exception as e:
    print(f"Error resolving address: {e}")




readableMACaddress = ''.join(['%02X' % i for i in wifi.radio.mac_address])
print("MAC Address:", readableMACaddress)


if True:

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
        print("Flags: {0}\nRC: {1}".format(flags, rc))


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


    ca_cert = "-----BEGIN CERTIFICATE-----" \
"MIIFvDCCA6SgAwIBAgIGICIHIAABMA0GCSqGSIb3DQEBCwUAMHUxCzAJBgNVBAYT" \
"AkJSMQ8wDQYDVQQIDAZQYXJhbmExHTAbBgNVBAcMFFNhbyBKb3NlIGRvcyBQaW5o" \
"YWlzMREwDwYDVQQKDAhTZWN1cml0eTETMBEGA1UECwwKV2ViIFNlcnZlcjEOMAwG" \
"A1UEAwwFTXkgQ0EwHhcNMjIwNzIwMjIxNDE2WhcNMzIwNzE3MjIxNDE2WjB1MQsw" \
"CQYDVQQGEwJCUjEPMA0GA1UECAwGUGFyYW5hMR0wGwYDVQQHDBRTYW8gSm9zZSBk" \
"b3MgUGluaGFpczERMA8GA1UECgwIU2VjdXJpdHkxEzARBgNVBAsMCldlYiBTZXJ2" \
"ZXIxDjAMBgNVBAMMBU15IENBMIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKC" \
"AgEAyuJosNZ4Qo2kUrtLq+r1tIcrZkVDU7olSSo716sfQBR7yK8S7Ay41LBwDKk9" \
"Fb1qGaa6/fQl8rlXpWpvex3rLdat9/6yg9Is1TeRerokiMTXIZ09ZBJToLZuReIH" \
"IJsKEqRfImJ71c1vwnWIZ5OWnMNm40KNHK2EkMrqIMlZkxZn83qyDfbhbITRsSmx" \
"EOUumq0wZpTOLCQvDOduDmR8EuvfVevn+BYyfve5veSSc1g/UtKfYGQ3QeSALpm1" \
"hVQxJW9ASjNHqfLBhVc6s9S1QsIaskslomMSYZsXyj0kIHVap+fa4VXFWVmLGfc6" \
"kZ1/vzUAGnAGhPG6CzdcA7Ow6F4WhvY/bB/s5kFbo9NGwRFFcQPVOOuIWUlpP1td" \
"HLbsjS/LP/ilhoo91+qkLOo3zY+u2eotsbLdFge99bjNu5QehuHEy8fu6iQhHUwV" \
"FFI8EJj8aeM5DRKxRDf3DZsT3PY+OOaV/u7iMp938xZyLdIO4M0xTnEbF6yYnPX8" \
"BLUXfrEdlsaAw13kAu681MGZpCUwinZgUID4yRoi5aF9juu6pO5oyEterNbXjjes" \
"gZakNNI4rGlku3th/R9nvl/W/VYq+fJxUDHzt6nxO3CJv/Fvsm3jcxhk932lf2Cb" \
"iMN4Y3TlVeSTl7fV46i/9F+K8wjJ0Na3xuQu6dU/dYD5isECAwEAAaNSMFAwHQYD" \
"VR0OBBYEFGmquj2JMPB7ccsUnui5BFEXz4z6MA8GA1UdEwEB/wQFMAMBAf8wCwYD" \
"VR0PBAQDAgEGMBEGCWCGSAGG+EIBAQQEAwIBBjANBgkqhkiG9w0BAQsFAAOCAgEA" \
"pKdHNauUQuwcsrzUzsRwMykieMimB0OAMU7qf2snv3Gxc7Tj4K4n7TyD0oa7WQAz" \
"jSx2urxd5RAOdz7g8sd2bygyLDsLrtUekWcVpnrBD4MIIvMEgL0KVtpKdyyFU+Ru" \
"WiUdKjQ48Nw6I8LfS61WJ3q35SmK//iB5PZr9TRZwMtyV1d9HMAyFJZaU4TJyA1h" \
"hdZCWTl2Qs/wX2JTUj2x8NsUbpDd/U1Fg0UD8ORblOrGBmTLD1T218l1rjinAaX7" \
"206U92VAOdaPQq+AEYDfQYSmohebZVayEktg5JW8xVGXLQNYUpzrJPQbzlkaAjBc" \
"R0sbeJmmGNG0Ii22ngmXthToA/gO7tSdhoA/SsNyxnK+OK/FrpjU6BJm2mHphQAk" \
"Suh7d/cbHPJGlY6HCrfrnT4SnLrOur9Q9Vwxps/D9+1NsYQm+xhEHZE/foJt66K6" \
"c5kDjKTGZKPJ4VW7bOM3SWfAfdBdB+YT0gKa8vXjgygdYWc2Bne0YKmS8dqFvh5N" \
"pjaMEfJgZpRP4vSxLdTCb2X2Y2Xt0PP6kRT+XBxtHQTdqxclNXA4bOyiyfndb4UC" \
"yqVCwkmVHzbFKAInSKcK6P8/K5kqBxNz7XojuJyaVKTnhSoFAy3A0R10f4oHkdsn" \
"p3p1LzOM0/rQPUMhwImzD8VgcelkfTHeif4ue1wEE2A=                    " \
"-----END CERTIFICATE-----                                       " \

    my_ssl_context = ssl.create_default_context()
    my_ssl_context.load_cert_chain("client.crt","client.key")
    my_ssl_context.load_verify_locations(None,None,ca_cert)
    # my_ssl_context.load_cert_chain(None,None)

if True:

    import adafruit_minimqtt.adafruit_minimqtt as MQTT # type: ignore

    # Set up a MiniMQTT Client
    mqtt_client = MQTT.MQTT(
        broker=broker,
        port=mqttport,
        username=mqttuser,
        password=mqttpass,
        socket_pool=pool,
        ssl_context=my_ssl_context,
        is_ssl=True
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

############# Stop here for now.


# while True:
#     print("sleep")
#     time.sleep(100.0)

if False:
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
            myaddress = [hex(device_address) for device_address in bus.scan()][0]
            bus.unlock()

        time.sleep(2)
    else:
        print("No valid I2C bus found.")


# import Adafruit_CircuitPython_TCS34725.adafruit_tcs34725 as TCS

if False:
    import adafruit_tcs34725

    # Create sensor object, communicating over the board's default I2C bus
    i2c = board.I2C()  # uses board.SCL and board.SDA
    # i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
    # sensor = TCS.TCS34725(i2c)
    sensor = adafruit_tcs34725.TCS34725(i2c,myaddress)


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
