from os import makedirs
from os.path import join, dirname
from ..encrypter import Encrypter

def test_encryption_workflow():
	mockClearFileFilePath = join(dirname(__file__), "mock/ninja.png")
	enc = Encrypter()

	with open(mockClearFileFilePath, "rb") as mockClearFD:
		data = mockClearFD.read()
		encryptedData = enc.encryptData(data, "ILoveRamen")
		decryptedData = enc.decryptData(encryptedData, "ILoveRamen")
		assert data == decryptedData
