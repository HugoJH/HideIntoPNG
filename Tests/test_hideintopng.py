from ..hideintopng import HideIntoPNG

from os.path import join, dirname, basename


def test_hide_into_png_workflow():

    payloadFilePath = join(dirname(__file__), "mock/ramen.png")
    containerPNGFilePath = join(dirname(__file__), "mock/ninja.png")

    hip = HideIntoPNG()

    hiddenPayload = b''
    with open(containerPNGFilePath, "rb") as containerFD:
        with open(payloadFilePath, "rb") as payloadFD:
            hiddenPayload = hip.hide(containerFD.read(), basename(payloadFilePath).encode('utf-8'), payloadFD.read(), "ILoveRamen")

    extractedPayload = hip.extract(hiddenPayload, "ILoveRamen")

    with open(payloadFilePath, "rb") as mockFD:
        assert(extractedPayload['data'] == mockFD.read())
    assert(extractedPayload['meta'] == basename(payloadFilePath).encode('utf-8'))