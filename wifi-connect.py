import network
import time
from picozero import pico_temp_sensor
from simple import MQTTClient
import micropython
# from micropython import const
import urequests 
from machine import Pin
from settings import SSID, PASSWORD, BROKER, PORT

# import paho.mqtt.client as mqtt
# from umqttsimple import MQTTClient


ssid = SSID
password = PASSWORD
adcpin = 4
sensor = machine.ADC(adcpin)
broker_address = BROKER  # Use the address of your local MQTT broker
port = 8883                 # Default MQTT port
client = MQRRClient
client.on_connect=on_connect(broker_address,port)
client.connect()


def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while not wlan.isconnected() and wlan.status() >= 0:
        print("Waiting to connect:")
        time.sleep(1)
        print(wlan.ifconfig())


def ReadTemperature():
    adc_value = sensor.read_u16()
    volt = (3.3/65535) * adc_value
    temperature = 27 - (volt - 0.706)/0.001721
    return round(temperature, 1)


connect
while True:
    temperature = ReadTemperature()
    print(temperature)
    time.sleep(5)
