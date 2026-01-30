import network
import usocket
from time import time, sleep
from umqtt.simple import MQTTClient
import machine
from picozero import pico_temp_sensor
from machine import Pin
import micropython
import ustruct as struct

adcpin = 4
sensor = machine.ADC(adcpin)
sock = usocket
SSID = ''
PASSWORD = b''
broker_address = b'e5d2174059b64286bd5f243dd055355a.s1.eu.hivemq.cloud'
mqtt_username = b"CB_1986"
mqtt_password = b'Cbaines123!'
TOPIC = b"data1"
wlan = network.WLAN(network.STA_IF)
mqtt = MQTTClient
#addr = usocket.getaddrinfo(192.168.1.11:80)[0][-1]
sock = socket.socket()
#s.bind(addr)
#s.listen()


def connect_to_wifi():
    SSID = 'BB'
    PASSWORD = b'6KH1jk1mn0s'
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    print("Connecting to Wi-Fi...")
    while not wlan.isconnected():
        time.sleep(1)
        print("Waiting for connection...")
    else:
        print("Wi-Fi connected!")
        print("IP address:", wlan.ifconfig())


def connectMQTT():
    client = MQTTClient(client_id=mqtt_username)
    server=broker_address
    port=0
    user=mqtt_username
    password=mqtt_password
    keepalive=2000
    ssl=False
    client.connect()
    return client


client = connectMQTT


def ReadTemperature():
    adc_value = sensor.read_u16()
    volt = (3.3/65535) * adc_value
    temperature = 27 - (volt - 0.706)/0.001721
    temp = round(temperature, 1)
    return temp


def send_data():
    try:
        print("Sending data...")
        ReadTemperature()
 #       client.connect()
        payload = str(temp)
        mqtt._send_str('8884', payload)
        client.publish(TOPIC, payload)
        mqtt.publish('CB_1986', 'data1', payload)
        print("Response code:", response.status_code)
        print("Response body:", response.text)
#       client.publish(temp)
    except Exception as e:
        print("Failed to send data:", e)

    return print("IP address:", wlan.ifconfig())

temp = ReadTemperature()
connect_to_wifi()
send_data()


while wlan.active(True):
    ReadTemperature()
    connect_to_wifi()
    send_data()

else:
    print("disconnected")
