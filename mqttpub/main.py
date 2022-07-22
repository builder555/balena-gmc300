
class MQTTClient:
    def __init__(self, mqtt, host='mqtt', port=1883, username='', password=''):
        try:
            self.client = mqtt.Client()
            if username:
                self.client.username_pw_set(username, password)
            self.client.connect(host, port, keepalive=60)
        except:
            raise Exception('MQTT broker is unreachable')
    def publish(self, topic, payload):
        msg = self.client.publish(topic=topic, payload=payload)
        if not msg.is_published():
            self.client.reconnect()
            self.client.publish(topic=topic, payload=payload)
    def __del__(self):
        self.client.disconnect()