import paho.mqtt.client as mqtt
import json
import time
#from sense_hat import SenseHat
from datetime import datetime
from collections import deque
import numpy as np
import pandas
import sqlite3
import csv
from csv import writer, reader, DictWriter
from statistics import mean
import ssl
import mycallbacks


temp_100 = deque([], maxlen=100)
humid_100 = deque([], maxlen=100)
temp_c_100 = deque([], maxlen=100)
humidity_100 = deque([], maxlen=100)

AIO_SERVER = b'io.adafruit.com'
AIO_PORT = 1883
AIO_USER = b'CuthbertB'
AIO_KEY = b'Secret_KEY!!!'
AIO_FEED = b'24hour_averages'

json_data = '{"name": "pico_W", "Temperature_c": "30.4", "Humidity": "48.3"}'
decoder = json.JSONDecoder()

# MQTT broker details
broker_address = "localhost"
# Create an MQTT client instance
client = mqtt.Client("catch_data")
client = mqtt.Client(client_id="Zero_hub", userdata=None, protocol=mqtt.MQTTv5)
client.connect(broker_address)
topic = "pico_W"
topic2 = "pico2w"
client.subscribe(topic)
client.subscribe(topic2)
port = 1883
csvfile = "pico_W.csv"
csvfile2 = "pico2w.csv"


def write_to_csv(file_name, var2, var3):
    var1 = datetime.now().isoformat()
    # Open the CSV file in append mode
    with open(file_name, 'a', newline='') as file_name:
        # Create a CSV writer object
        writer1 = csv.writer(csvfile)
        # Write the variables as a single line
        writer1.writerow([var1, var2, var3])
    # Read the data point from the CSV file


def calculate_rolling_averagemean(data):
    total = sum(data)
    num1 = len(data)
    aveMean = total / num1
#   ave1 = mean([data_window])
#   print(ave)
    return aveMean
# Run the while loop for the specified duration


def truncate_float(value, digits_after_point=2):
    pow_10 = 10 ** digits_after_point
    return (float(int(value * pow_10))) / pow_10
# this limits the number of decimal places used.


def on_message(client, userdata, messsage, properties=None):
    print(" Received message " + str(message.payload)
          + "topic = " + message.topic)
    decoded_message = json.loads(message.payload)
    file_name = str(decoded_message["name"])
    temperature = truncate_float(float(decoded_message["Temperature_c"]))
    humidity = truncate_float(float(decoded_message["Humidity"]))
    if file_name == topic:
        temp_100.appendleft(temperature)
        ave_temp = calculate_rolling_averagemean(temp_100)
        humid_100.appendleft(humidity)
        ave_humid = calculate_rolling_averagemean(humid_100)
        print(ave_temp, ave_humid)
    elif file_name == topic2:
        temp_c_100.appendleft(temperature)
        ave_temp_c = calculate_rolling_averagemean(temp_c_100)        
        humidity_100.appendleft(humidity)
        ave_humidity = calculate_rolling_averagemean(humidity_100)
        print(ave_temp_c, ave_humidity)
    else:
        print("Error")

    var2 = temperature
    var3 = humidity
    write_to_csv(file_name, var2, var3)
    print("message proccessed")


def on_connect():
    print("connected")


def on_subscribe():
    print("subscribed")


def on_publish():
    print("published")


client.on_message = mycallbacks.on_message
client.on_connect = mycallbacks.on_connect
client.on_publish = mycallbacks.on_publish
client.on_subscribe = mycallbacks.on_subscribe


def send_data(data1):
    client = mqtt.Client(AIO_USER, AIO_SERVER, port=AIO_PORT, user=AIO_USER,
                         password=AIO_KEY)
    client.connect()
    client.publish('{}.feeds.{}'.format(AIO_USER, AIO_FEED), tuple(data1))
    client.disconnect()


start_time = time.time()
duration = 4000
while (time.time() - start_time) < duration:
    ave_temp = calculate_rolling_averagemean(temp_100)
    ave_humid = calculate_rolling_averagemean(humid_100)
    ave_temp_c = calculate_rolling_averagemean(temp_c_100)
    ave_humidity = calculate_rolling_averagemean(humidity_100)            
    data1 = {
        "pico_W_ave_temp": {ave_temp},
        "pico_W_ave_humid": {ave_humid},
        "pico2w": {ave_temp_c},
        "pico2w": {ave_humidity}
    }
    send_data(data1)
    print(f"Published: {data1} to topic: {AIO_SERVER}")
# Sleep for a short duration if needed
    time.sleep(30)
    duration = duration + 100
# Disconnect from the MQTT broker
else:
    client.disconnect()
