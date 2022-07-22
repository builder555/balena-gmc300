import pytest
from unittest.mock import MagicMock, call
from .main import MQTTClient

def make_mqtt(client):
    m = MagicMock()
    m.Client.return_value=client
    m.client_instance = client
    return m
    
@pytest.fixture
def fake_mqtt():
    return make_mqtt(MagicMock())

@pytest.fixture
def bad_mqtt():
    bad_result = MagicMock()
    bad_result.is_published.return_value=False
    bad_client = MagicMock()
    bad_client.publish = MagicMock(return_value=bad_result)
    return make_mqtt(bad_client)

@pytest.fixture
def broken_mqtt():
    bad_client = MagicMock()
    bad_client.connect = lambda *a, **kw: 1/0
    return make_mqtt(bad_client)
    

class TestWrapper:

    def test_raises_exception_if_broker_is_unavailable(self, broken_mqtt):
        with pytest.raises(Exception) as e:
            MQTTClient(broken_mqtt)
        assert str(e.value) == 'MQTT broker is unreachable'
    
    def test_connects_to_mqtt_server_on_init(self, fake_mqtt):
        MQTTClient(fake_mqtt, 'fake_host', 1883)
        fake_mqtt.client_instance.connect.assert_called_once_with('fake_host', 1883, keepalive=60)

    def test_can_publish_to_mqtt_topic(self, fake_mqtt):
        mqtt = MQTTClient(fake_mqtt)
        mqtt.publish(topic='my-topic', payload='my-payload')
        fake_mqtt.client_instance.publish.assert_called_once_with(topic='my-topic', payload='my-payload')

    def test_reconnects_if_publishing_fails(self, bad_mqtt):
        mqtt = MQTTClient(bad_mqtt)
        mqtt.publish(topic='my-topic', payload='my-payload')
        bad_mqtt.client_instance.reconnect.assert_called_once()
        bad_mqtt.client_instance.publish.assert_has_calls([
            call(topic='my-topic', payload='my-payload'),
            call(topic='my-topic', payload='my-payload'),
        ])

    def test_can_specify_username_and_password(self, fake_mqtt):
        MQTTClient(fake_mqtt, username='fake_user', password='fake_pass')
        fake_mqtt.client_instance.username_pw_set.assert_called_once_with('fake_user', 'fake_pass')

    def test_disconnects_when_done(self, fake_mqtt):
        MQTTClient(fake_mqtt)
        fake_mqtt.client_instance.disconnect.assert_called_once()
    