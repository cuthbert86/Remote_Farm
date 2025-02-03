import time
from sense_hat import SenseHat
from azure.iot.device import IoTHubDeviceClient, Message

# Initialize Sense HAT
sense = SenseHat()

# Azure IoT Hub connection string
CONNECTION_STRING = "HostName=cuthbert-hub.azure-devices.net;DeviceId=Cuthbert1;SharedAccessKey=Uy+5ez0ZseOvICsiYhT6iOL9upLgOeLbiAIoTMO2Bw4="

# Initialize the IoT Hub client
client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)


def collect_and_send_data():
    while True:
        # Collect data from Sense HAT
        temperature = sense.get_temperature()
        humidity = sense.get_humidity()
        pressure = sense.get_pressure()

        # Create a message payload
        message = {
            "temperature": temperature,
            "humidity": humidity,
            "pressure": pressure
        }

        # Convert the message payload to a JSON string
        message_json = str(message)

        # Send the message to the Azure IoT Hub
        client.send_message(message_json)
        print("Message successfully sent: {}".format(message_json))

        # Wait for a while before sending the next message
        time.sleep(10)


def main():
    try:
        print("Starting data collection from Sense HAT...")
        collect_and_send_data()
    except KeyboardInterrupt:
        print("Data collection stopped.")
    finally:
        # Clean up the IoT Hub client
        client.shutdown()


if __name__ == "__main__":
    main()