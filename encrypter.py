from Crypto import Random
from Crypto.Cipher import AES
import hashlib

class Encrypter:

    AES_ALIGNMENT = 16
    ITERATIONS = 42
    SALT_SIZE = 16

    def encryptData(self, data, passphrase):
        salt = Random.get_random_bytes(self.SALT_SIZE)

        key = self._generateKey(bytearray(passphrase.encode('utf-8')) + bytearray(salt), self.ITERATIONS)
        cipher = AES.new(key, AES.MODE_ECB)
        paddedClearData = self._padData(data, self.AES_ALIGNMENT)
        encryptedData = cipher.encrypt(paddedClearData)

        return salt + encryptedData

    def decryptData(self, encryptedData, passphrase):
        salt = encryptedData[0:self.SALT_SIZE]
        unsaltedEncryptedData = encryptedData[self.SALT_SIZE:]
        key = self._generateKey(bytearray(passphrase.encode('utf-8')) + bytearray(salt), self.ITERATIONS)
        cipher = AES.new(key, AES.MODE_ECB)

        return self._unpadData(cipher.decrypt(unsaltedEncryptedData))


    def _padData(self, data, alignment):
        padding_size = alignment - len(data) % alignment
        padding = bytes([padding_size]) * padding_size
        return data + padding

    def _unpadData(self, paddedData):
        paddingSize = paddedData[-1]
        return paddedData[:-paddingSize]

    def _generateKey(self, saltedPassPhrase, iterations):
        assert iterations > 0

        for i in range(iterations):
            saltedPassPhrase = hashlib.sha256(saltedPassPhrase).digest()

        return saltedPassPhrase
