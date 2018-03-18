from os import makedirs
from os.path import exists, join, dirname, basename
from shutil import rmtree

from ..hideintopng.embedder import Embedder


def test_insert_payload():
    _resetResultsFolder()
    embedder = Embedder()
    containerFilePath = join(dirname(__file__), "mock/ninja.png")
    payloadFilePath = join(dirname(__file__), "mock/ramen.png")
    mockfileFilePath = join(dirname(__file__), "mock/ninjaThatAteTheRamen.png")

    containerData = b''
    with open(containerFilePath, "rb") as containerFD:
        containerData = containerFD.read()

    payloadData = b''
    with open(payloadFilePath, "rb") as payloadFD:
        payloadData = payloadFD.read()

    result = embedder.insertPayload(containerData, basename(payloadFilePath).encode('utf-8'), payloadData)
    with open(mockfileFilePath, "rb") as mockFD:
        assert mockFD.read() == result

def test_extract_payload():
    _resetResultsFolder()
    embedder = Embedder()

    containerFilePath = join(dirname(__file__), "mock/ninjaThatAteTheRamen.png")

    payload = b''
    with (open(containerFilePath, "rb")) as containerFD:
        payload = embedder.extractPayload(containerFD.read())

    with open(join(dirname(__file__), "mock/", "ramen.png"),"rb") as mockFD:
        assert payload['data'] == mockFD.read()

def _resetResultsFolder():
    if exists(join(dirname(__file__), "results")):
        rmtree(join(dirname(__file__), "results"))
    makedirs(join(dirname(__file__), "results"))
