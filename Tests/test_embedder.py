from ..embedder import Embedder
from os import makedirs
from os.path import exists, join, dirname
from shutil import rmtree

def test_insert_payload():
    _resetResultsFolder()
    embedder = Embedder()
    containerFilePath = join(dirname(__file__), "mock/ninja.png")
    payloadFilePath = join(dirname(__file__), "mock/ramen.png")
    mockfileFilePath = join(dirname(__file__), "mock/ninjaThatAteTheRamen.png")
    result = embedder.insertPayload(containerFilePath, payloadFilePath)
    with open(mockfileFilePath, "rb") as mockFD:
        assert mockFD.read() == result

def test_extract_payload():
    _resetResultsFolder()
    embedder = Embedder()

    containerFileFilePath = join(dirname(__file__),
        "mock/ninjaThatAteTheRamen.png")

    payload = embedder.extractPayload(containerFileFilePath)

    with open(join(dirname(__file__), "mock/", "ramen.png"),"rb") as mockFD:
        assert payload['data'] == mockFD.read()

def _resetResultsFolder():
    if exists(join(dirname(__file__), "results")):
        rmtree(join(dirname(__file__), "results"))
    makedirs(join(dirname(__file__), "results"))
