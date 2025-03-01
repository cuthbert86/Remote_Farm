# This is my "main.py" micropython program, it needs to be so smooth that it will run and run for weeks at a time while the pico has power.
# It connects to the internet, collects data and I'd like it to connect to the adafruit IOT ckoud server but there is a bug in the micropython firmware that
won't let it connect to a public network (and I'm smart enough to fix it - yet).  So maybe mext week I'll convet this program into circuit python which should be 
compatible.  
import time
from helper import GetTemperature, connect_to_wifi, WifiServer, to_json, collect_sensor_data, write_to_csv, calculate_mean
import usocket
import socket
from time import time, sleep
import network
import time
from umqtt.simple import MQTTClient
import machine
from picozero import pico_temp_sensor
from machine import Pin
import micropython
import ustruct as struct
import json
import random
import socket
import uos
import time
from machine import I2C, Pin
from I2C_LCD import I2CLcd
from collections import deque
from LCD_API import LcdApi

#(AIO_USER, AIO_SERVER, port=AIO_PORT, user=AIO_USER, password=AIO_KEY)
AIO_SERVER = b'io.adafruit.com'
AIO_PORT = 1883
AIO_USER = b'CuthbertB'
AIO_KEY = b'Secret_KEY!!!'
AIO_FEED = b'datalog'

dq = deque((), 100)
#bbutton = Pin(16, Pin.IN, Pin.PULL_UP) 
Self_Name = 'PW_1'
ssidAP         = 'CuthbertWifi' #Enter the router name
passwordAP     = '999'  # Enter the router password
local_IP       = '192.168.1.1'
gateway        = '192.168.1.1'
subnet         = '255.255.255.0'
dns            = '8.8.8.8'
sta_if = network.WLAN(network.STA_IF)
ap_if = network.WLAN(network.AP_IF)
adcpin = 4
sensor = machine.ADC(adcpin)
sock = usocket
SSID = 'BB'
PASSWORD = '6KH1jk1mn0s'
i2c = I2C(1, sda=Pin(14), scl=Pin(15), freq=400000)
devices = i2c.scan()
#lcd = I2CLcd(i2c, devices[0], 2, 16)
#lcd.display_off
USER = "Cuthbert"

wlan = network.WLAN(network.STA_IF)
TOPIC = "test_data"
#mqtt = MQTTClient
#sending = broker_address
#BROKER = "192.168.4.16"
#PORT = 1883  # Topic to publish to
#CLIENT_ID = "Cuthbert"
Temperature = GetTemperature()
timestamp = time.time()

csv_data = collect_sensor_data()
print(csv_data)

def send_data(value):
    client = MQTTClient(AIO_USER, AIO_SERVER, port=AIO_PORT, user=AIO_USER, password=AIO_KEY)
    client.connect()
    client.publish('{}.feeds.{}'.format(AIO_USER, AIO_FEED), str(value))
    client.disconnect()


def LCD_show(csv_data):
    i2c = I2C(1, sda=Pin(14), scl=Pin(15), freq=400000)
    devices = i2c.scan()
    
    if devices != []:
        Icd = I2CLcd(i2c, devices[0], 2, 16)
        Icd.move_to(0, 0)
        string_temp = str(csv_data)
        Icd.putstr(csv_data)
#        Icd.move_to(0, 1)
#        Icd.putstr()
        time.sleep(10)
        Icd.display_off
    else:
        print("No address found")


def calculate_mean(dq):
    calculate = sum(dq) / len(dq)
    return calculate


start_time = time.time()
duration = 4000
"""
while True:
    if not button.value():
        LCD_show(str(Temperature), i2c, devices)
    else:
        pass
"""
try:
    print("Connecting to MQTT broker...")
#    client.connect()
    dq.appendleft(Temperature)
    print("Connected to MQTT broker.")
    dq.appendleft(Temperature)
    mean = calculate_mean(dq)
    print(mean)
    while (time.time() - start_time) < duration:
        LCD_show(str(csv_data))
        Temperature = GetTemperature()
        timestamp = time.time()
#        send_data(GetTemperature())
        csv_data = collect_sensor_data()
        write_to_csv(csv_data)
        dq.appendleft(Temperature)
        print(list(dq))
        mean = calculate_mean(dq)
        print(mean)        
        LCD_show(str(csv_data))
        print(csv_data)
#        send_data(csv_data)
#        client.publish(TOPIC, json_result)
        time.sleep(10)  # Publish every 5 seconds
        Temperature = GetTemperature()
        csv_data = collect_sensor_data()
        write_to_csv(csv_data)
        timestamp = time.time()
 #       json_result = to_json(Self_Name, Temperature,timestamp)
        dq.appendleft(Temperature)
        print(list(dq))
        print(csv_data)
 #       client.publish(TOPIC, json_result)
        time.sleep(10)
        Temperature = GetTemperature()
        timestamp = time.time()
 #       json_result = to_json(Self_Name, Temperature, timestamp)
        csv_data = collect_sensor_data()
        write_to_csv(csv_data)        
        dq.appendleft(Temperature)
        print(list(dq))
        mean = calculate_mean(dq)
        print(mean)
        LCD_show(str(csv_data))
        print(csv_data)
  #      client.publish(TOPIC, json_result)
        Temperature = GetTemperature()
        timestamp = time.time()
  #      json_result = to_json(Self_Name, Temperature, timestamp)
        csv_data = collect_sensor_data()
        write_to_csv(csv_data)
        dq.appendleft(Temperature)
        print(list(dq))
        print(csv_data)
  #      client.publish(TOPIC, json_result)
 #       send_data(csv_data)
except Exception as e:
    print("An error occurred:", e)
#    client.disconnect()
#    wlan.disconnect() 
