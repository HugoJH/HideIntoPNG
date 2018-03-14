from ..embedder import Embedder
from os import makedirs
from os.path import exists, join, dirname
from shutil import rmtree
from filecmp import cmp

def test_insert_payload():
    _resetResultsFolder()
    embedder = Embedder()
    containerFilePath = join(dirname(__file__), "mock/ninja.png")
    payloadFilePath = join(dirname(__file__), "mock/ramen.png")
    resultFilePath = join(dirname(__file__), "results/ninjaThatAteTheRamen.png")
    mockfileFilePath = join(dirname(__file__), "mock/ninjaThatAteTheRamen.png")
    embedder.insertPayload(containerFilePath, payloadFilePath, resultFilePath)
    assert cmp(mockfileFilePath, resultFilePath, shallow=False)

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
