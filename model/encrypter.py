from cryptography.fernet import Fernet
import base64

class Encrypter:
    key = b'Gg91BbmzEad1OyTOGF4wdQNWcmuOlNcvY4-rpHtK3YE='

    def bytesToString(self, dataBytes):
        str = dataBytes.decode('utf-8')
        return str

    def stringToBytes(self, dataString):
        dataBytes = bytes(dataString, 'UTF-8')
        return dataBytes

    def encrypt(self, data):
        bytes = self.stringToBytes(data)
        f = Fernet(self.key)
        data = f.encrypt(bytes)
        dataReturned = self.bytesToString(data)
        return dataReturned

    def decrypt(self, data):
        bytes = self.stringToBytes(data)
        f = Fernet(self.key)
        data = f.decrypt(bytes)
        dataReturned = self.bytesToString(data)
        return dataReturned