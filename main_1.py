
from helper import GetTemperature, connect_to_wifi, WifiServer, to_json
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


USER = "Cuthbert"

wlan = network.WLAN(network.STA_IF)
TOPIC = "test_data"
mqtt = MQTTClient
#sending = broker_address
BROKER = "192.168.1.17"
PORT = 1883  # Topic to publish to
CLIENT_ID = "Cuthbert"
Temperature = GetTemperature()
json_string = '{"temp":"27"}'
data1 = json.loads(json_string)


ip = connect_to_wifi()
gateway1 = WifiServer('CuthbertWifi', '999')
client = MQTTClient(CLIENT_ID, BROKER)
start_time = time.time()
duration = 4000
try:
    print("Connecting to MQTT broker...")
    client.connect()
    print("Connected to MQTT broker.")

    while (time.time() - start_time) < duration:

        Temperature = GetTemperature()
        json_result = to_json(Temperature)
        print (json_result)
#        client.publish(TOPIC, json_result)
        time.sleep(10)  # Publish every 5 seconds
        Temperature = GetTemperature()
        json_result = to_json(Temperature)
        print(json_result)
 #       client.publish(TOPIC, json_result)
        time.sleep(10)
        Temperature = GetTemperature()
        json_result = to_json(Temperature)
        print (json_result)
  #      client.publish(TOPIC, json_result)
        Temperature = GetTemperature()
        json_result = to_json(Temperature)
        print (json_result)
  #      client.publish(TOPIC, json_result)
        
except Exception as e:
    print("An error occurred:", e)
    client.disconnect()
    wlan.disconnect()
