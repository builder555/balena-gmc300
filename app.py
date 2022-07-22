import glob
import serial
import os
from time import sleep
from gmc300 import GMC300
from mqttpub import MQTTClient
import paho.mqtt.client as paho_mqtt
from contextlib import contextmanager
from dataclasses import dataclass

class ExceptionNoSerialPort(Exception):
    pass

@contextmanager
def get_serial_port():
    print('detecting port...')
    devices = glob.glob('/dev/*usb*') + glob.glob('/dev/*USB*')
    for dev in devices:
        try:
            with serial.Serial(dev, 57600, timeout=2) as p:
                print(f'port detected: {dev}')
                yield p
                break
        except:
            continue
    else:
        raise ExceptionNoSerialPort

@dataclass
class Monitor():
    geiger: GMC300
    read_period: int
    notification_cooldown: int
    cpm_limit: int
    mqtt_topic: str
    mqtt_host: str
    mqtt_user: str = ''
    mqtt_pass: str = ''
        
    def run(self):
        geiger = self.geiger
        print('Version:', geiger.get_version())
        while True:
            cpm = geiger.get_cpm()
            if cpm == 0:
                geiger.power_on()
                sleep(40)
                cpm = geiger.get_cpm()
            print(f'CPM: {cpm}')
            if cpm >= self.cpm_limit:
                message = f'☢️WARNING: {cpm}CPM☢️'
                MQTTClient(
                    mqtt=paho_mqtt,
                    host=self.mqtt_host,
                    username=self.mqtt_user,
                    password=self.mqtt_pass,
                ).publish(topic=self.mqtt_topic, payload=message)
                sleep(self.notification_cooldown)
            sleep(self.read_period)
        

def main():
    with get_serial_port() as port:
        geiger = GMC300(port)
        Monitor(
            geiger = geiger,
            read_period = int(os.getenv('READ_PERIOD', '5')),
            notification_cooldown = int(os.getenv('NOTIFICATION_COOLDOWN', '30')),
            cpm_limit = int(os.getenv('CPM_LIMIT', '100')),
            mqtt_topic = os.getenv('MQTT_TOPIC', 'CPM_ALERT'),
            mqtt_host = os.getenv('MQTT_HOST', 'mqtt'),
            mqtt_user = os.getenv('MQTT_USER', ''),
            mqtt_pass = os.getenv('MQTT_PASS', ''),
        ).run()

if __name__ == '__main__':
    try:
        main()
    except ExceptionNoSerialPort:
        print('No USB serial port detected, please ensure the device is connected')
