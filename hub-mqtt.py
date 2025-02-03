import paho.mqtt.client as mqtt
# import mqtt
import json
import time
from sense_hat import SenseHat
from datetime import datetime
from collections import deque
# from array import *
import numpy as np
# import pandas
import sqlite3
import csv
from csv import writer, reader, DictWriter
# from statistics import mean

# CSV file path
csvfile = "store2.csv"
sense = SenseHat()
json_string = '{"temp": "36.24469757080078", "Humidity": "37.37043380737305", "Date": "2024-03-22 00:13:27.122036"}'
data1 = json.loads(json_string)
# Initialize deque with 120 None values
data_window = deque([], maxlen=120)
data_week = deque([], maxlen=840)
data_month = deque([], maxlen=3360)


# Now you can access the data fields individually
temperature = float()
humidity = float()
date = data1["Date"]
day = float()
week = float()
month = float()
port = 1883
# MQTT broker details
broker_address = "192.168.1.11"     
temp1 = float()
# Create an MQTT client instance
client = mqtt.Client()
conn = sqlite3.connect('sensor_data.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS sensor_data
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   temperature REAL,
                   humidity REAL,
                   pressure REAL,
                   timestamp TEXT)''')
# Connect to the MQTT broker
client.connect(broker_address, port)
cursor = conn.cursor()
# Define the topic to which you want to publish
topic = "data_1"

start_time = time.time()
duration = 4000
# client.subscribe(topic="test_data")


def write_to_csv(file_name, var1, var2, var3, var4):
    # Open the CSV file in append mode
    with open(file_name, 'a', newline='') as csvfile:
        # Create a CSV writer object
        writer1 = csv.writer(csvfile)
        # Write the variables as a single line
        writer1.writerow([var1, var2, var3, var4])
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


while (time.time() - start_time) < duration:
    data_window.appendleft(truncate_float(sense.get_temperature()))
    data_week.appendleft(truncate_float(sense.get_temperature()))
    data_month.appendleft(truncate_float(sense.get_temperature()))
    temp = truncate_float(sense.get_temperature())
    humidity = truncate_float(sense.get_humidity())
    Pressure = truncate_float(sense.get_pressure())
    timestamp = datetime.now().isoformat()
    rolling_avg = truncate_float(calculate_rolling_averagemean(data_window))
    ave2 = truncate_float(calculate_rolling_averagemean(data_week))
    ave3 = truncate_float(calculate_rolling_averagemean(data_month))

    data1 = {"temp": str(temp),
             "Humidity": str(humidity),
             "Pressure": str(Pressure),
             "Date": str(timestamp),
             "Ave1": str(rolling_avg),
             "AveWeek": str(ave2),
             "AveMonth": str(ave3),
             }
    write_to_csv(csvfile, temp, humidity, Pressure, timestamp)
    # Insert data into the table
    cursor.execute('''INSERT INTO sensor_data (temperature, humidity, pressure, timestamp)
                      VALUES (?, ?, ?, ?)''', (temperature, humidity, Pressure, timestamp))
    # Commit changes to the database
    conn.commit()
    print("Saved sensor data:", temp, humidity, Pressure, timestamp)
    message = json.dumps(data1)
# print (ave3)
    client.publish(message, topic)
    print(f"Published: {message} to topic: {topic}")
# Sleep for a short duration if needed
    time.sleep(10)
    print(f"Calculted Rolling averages: {data1}")
# Disconnect from the MQTT broker
else:
    client.disconnect()
