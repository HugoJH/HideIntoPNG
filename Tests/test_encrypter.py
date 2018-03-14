from os import makedirs
from os.path import exists, join, dirname
from shutil import rmtree
from ..encrypter import Encrypter

def test_encryption_workflow():
	_resetResultsFolder()
	mockClearFileFilePath = join(dirname(__file__), "mock/ninja.png")
	mockEncryptedFileFilePath = join(dirname(__file__), "mock/ninja.encrypted")
	enc = Encrypter()

	with open(mockClearFileFilePath, "rb") as mockClearFD:
		data = mockClearFD.read()
		encryptedData = enc.encryptData(data, "ILoveRamen")
		decryptedData = enc.decryptData(encryptedData,"ILoveRamen")
		assert data == decryptedData

def _resetResultsFolder():
    if exists(join(dirname(__file__), "results")):
        rmtree(join(dirname(__file__), "results"))
    makedirs(join(dirname(__file__), "results"))
