from .embedder import Embedder
from .encrypter import Encrypter

class HideIntoPNG():

	def hide(self, containerData, payloadMetaData, payloadData, passPhrase):
		emb = Embedder()
		enc = Encrypter()

		encryptedPayloadMeta = enc.encryptData(payloadMetaData, passPhrase)
		encryptedPayloadData = enc.encryptData(payloadData, passPhrase)

		return emb.insertPayload(containerData, encryptedPayloadMeta, encryptedPayloadData)

	def extract(self, containerWithPayloadData, passPhrase):
		emb = Embedder()
		enc = Encrypter()

		containerData = b''
		encryptedPayload = emb.extractPayload(containerWithPayloadData)

		payload = {}
		payload['meta'] = enc.decryptData(encryptedPayload['filename'], passPhrase)
		payload['data'] = enc.decryptData(encryptedPayload['data'], passPhrase)


		return payload


