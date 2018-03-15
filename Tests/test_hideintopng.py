from ..hideintopng import HideIntoPNG

from os.path import exists, join, dirname

def test_hide_into_png_workflow():

    payloadFilePath = join(dirname(__file__), "mock/ramen.png")
    containerPNGFilePath = join(dirname(__file__), "mock/ninja.png")
    mockResultFilePath = join(dirname(__file__), "mock/ninjaThatAteTheRamen.png")
    hip = HideIntoPNG()
    result = hip.hide(containerPNGFilePath, payloadFilePath)
    with open (mockResultFilePath, "rb") as mockFD:
        assert(result == mockFD.read())