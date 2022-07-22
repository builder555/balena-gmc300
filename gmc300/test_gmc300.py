import pytest
from .main import GMC300

FAKE_VERSION = 'GMC300'
FAKE_SERIAL = 0x123456789ABC
FAKE_CPM = 591

class FakeSerial:
    def __init__(self, port):
        self.written = b''
    def write(self, data):
        self.written = data
    def readline(self):
        if self.written == b'<GETVER>>':
            return FAKE_VERSION.encode()
        if self.written == b'<GETSERIAL>>':
            return FAKE_SERIAL.to_bytes(8, 'big')
        if self.written == b'<GETCPM>>':
            return FAKE_CPM.to_bytes(4, 'big')

@pytest.fixture
def gmc300():
    return GMC300(FakeSerial('/dev/ttyUSB0'))

class TestGMC300:
    def test_can_get_version(self, gmc300):
        serial = gmc300.get_version()
        assert serial == FAKE_VERSION
    def test_can_get_serial_number(self, gmc300):
        serial = gmc300.get_serial()
        assert serial.lstrip('0') == hex(FAKE_SERIAL)[2:].upper()
    def test_can_get_cpm(self, gmc300):
        cpm = gmc300.get_cpm()
        assert cpm == FAKE_CPM
    def test_can_power_on(self, gmc300):
        gmc300.power_on()
        assert gmc300.sr.written == b'<POWERON>>'
    def test_can_power_off(self, gmc300):
        gmc300.power_off()
        assert gmc300.sr.written == b'<POWEROFF>>'
