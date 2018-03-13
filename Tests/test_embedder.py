from ..embedder import Embedder
from os import makedirs
from os.path import exists, join, dirname
from shutil import rmtree
from filecmp import cmp

def test_insert_payload():
    if exists(join(dirname(__file__), "results")):
        rmtree(join(dirname(__file__), "results"))
    makedirs(join(dirname(__file__), "results"))

    embedder = Embedder()
    containerFilePath = join(dirname(__file__), "mock/ninja.png")
    payloadFilePath = join(dirname(__file__), "mock/ramen.png")
    resultFilePath = join(dirname(__file__), "results/ninjaThatAteTheRamen.png")
    mockfileFilePath = join(dirname(__file__), "mock/ninjaThatAteTheRamen.png")
    embedder.insertPayload(containerFilePath, payloadFilePath, resultFilePath)

    assert cmp(mockfileFilePath, resultFilePath, shallow=False)