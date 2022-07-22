class GMC300:
    def __init__(self, serial_port):
        self.sr = serial_port
    def get_version(self):
        cmd = "<GETVER>>"
        self.sr.write(cmd.encode())
        version = self.sr.readline()
        return version.decode()
    def get_serial(self):
        self.sr.write("<GETSERIAL>>".encode())
        serial = self.sr.readline()
        return  ''.join([hex(x)[2:] for x in serial]).upper()
    def get_cpm(self):
        self.sr.write("<GETCPM>>".encode())
        cpm = self.sr.readline()
        return int.from_bytes(cpm, 'big')
    def power_on(self):
        self.sr.write("<POWERON>>".encode())
    def power_off(self):
        self.sr.write("<POWEROFF>>".encode())
