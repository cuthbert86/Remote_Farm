# This is the main.py micropython program that will run and run while the pico W has power.
# It connects to the internet, collects data, connects to my own private mqtt broker and sends data to it.
import time
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
import uos

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
#BROKER = "192.168.4.16"
#PORT = 1883  # Topic to publish to
#CLIENT_ID = "Cuthbert"
Temperature = GetTemperature()
timestamp = time.time()
json_string = {"name":Self_Name,
                "temp":Temperature,
                "Timestamp":timestamp,
               }
print(json_string)


def collect_sensor_data():
    # Collect data from the sensor
    Temp = GetTemperature()
    
    # Get the current timestamp
    timestamp = time.time()
    
    # Format timestamp to YYYY-MM-DD HH:MM:SS
    formatted_time = time.localtime(timestamp)
    timestamp_str = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
        formatted_time[0], formatted_time[1], formatted_time[2], 
        formatted_time[3], formatted_time[4], formatted_time[5]
    )

    # Create a CSV formatted string
    csv_data = "{},{}\n".format(timestamp_str, Temp)
    
    return csv_data

csv_data = collect_sensor_data()
print(csv_data)

def write_to_csv(csv_data, filename="PW_1.csv"):
    # Write the CSV data to a file
    with open(filename, "a") as file:
        file.write(csv_data)


write_to_csv(csv_data)

json_data = json.dumps(json_string)
#data1 = json.loads(json_string)
ip = connect_to_wifi()
# gateway1 = WifiServer('CuthbertWifi', '999')
#client = MQTTClient(CLIENT_ID, BROKER)
start_time = time.time()
duration = 4000
try:
    print("Connecting to MQTT broker...")
#    client.connect()
    print("Connected to MQTT broker.")

    while (time.time() - start_time) < duration:

        Temperature = GetTemperature()
        timestamp = time.time()
        csv_data = collect_sensor_data()
        write_to_csv(csv_data)
#        json_result = to_json(Self_Name, Temperature, timestamp)
        print(csv_data)
#        client.publish(TOPIC, json_result)
        time.sleep(10)  # Publish every 5 seconds
        Temperature = GetTemperature()
        csv_data = collect_sensor_data()
        write_to_csv(csv_data)
 #       timestamp = time.time()
 #       json_result = to_json(Self_Name, Temperature,timestamp)
        print(csv_data)
 #       client.publish(TOPIC, json_result)
        time.sleep(10)
        Temperature = GetTemperature()
        timestamp = time.time()
 #       json_result = to_json(Self_Name, Temperature, timestamp)
        csv_data = collect_sensor_data()
        write_to_csv(csv_data)        
        print(csv_data)
  #      client.publish(TOPIC, json_result)
        Temperature = GetTemperature()
        timestamp = time.time()
  #      json_result = to_json(Self_Name, Temperature, timestamp)
        csv_data = collect_sensor_data()
        write_to_csv(csv_data)
        print(csv_data)
  #      client.publish(TOPIC, json_result)
        
except Exception as e:
    print("An error occurred:", e)
#    client.disconnect()
#    wlan.disconnect()
