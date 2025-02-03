import network
import socket
from time import sleep, time
from picozero import pico_temp_sensor, pico_led
import machine
from config import wifi_ssid, wifi_password, mqtt_server, mqtt_username, mqtt_password

ssid = 'BB'  # wifi name
password = '6KH1jk1mn0s'  # wifi password
temperature = 0
start_time = time()
duration = 400


def connect():
    # Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip


def open_socket(ip):
    # Open a socket
    address = (ip, 82)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection

    
def webpage(temperature, state):
    #Template HTML
    html = f"""
            <!DOCTYPE html>
            <html>
            <form action="./lighton">
            <input type="submit" value="Light on" />
            </form>
            <form action="./lightoff">
            <input type="submit" value="Light off" />
            </form>
            <p>LED is {state}</p>
            <p>Temperature is {temperature}</p>
            </body>
            </html>
            """
    return str(html)


def serve(connection):
    # Start a web server
    state = 'OFF'
    pico_led.off()
    temperature = 0
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        try:
            request = request.split()[1]
        except IndexError:
            pass
        if request == '/lighton?':
            pico_led.on()
            state = 'ON'
        elif request =='/lightoff?':
            pico_led.off()
            state = 'OFF'
        temperature = pico_temp_sensor.temp
        html = webpage(temperature, state)
        client.send(html)
        client.close()
        
try:
    ip = connect()
    connection = open_socket(ip)
    temperature = pico_temp_sensor.temp
except KeyboardInterrupt:
    machine.reset()
while (time() - start_time) < duration:
    serve
#    print(temperature, ip)
else:
    pass


