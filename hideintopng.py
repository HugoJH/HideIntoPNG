from .embedder import Embedder
from .encrypter import Encrypter

class HideIntoPNG():

	def hide(self, containerData, payloadMetaData, payloadData, passPhrase):
		"""
			Embeds data and metadata both encrypted with a passPhrase in a PNG container.

			Parameters:
				containerData (bin) -- Binary Data of a sample PNG file
				payloadMetaData (bin) -- Metadata to be encrypted and embeded in the ContainerData
				payloadMetaData (bin) -- data to be encrypted and embeded in the ContainerData
				passPhrase (str) -- password used to encrypt data and metadata before embed both in the ContainerData

			Returns:
				bin: ContainerData with Data and Metadata embedded within.
		"""

		emb = Embedder()
		enc = Encrypter()

		encryptedPayloadMeta = enc.encryptData(payloadMetaData, passPhrase)
		encryptedPayloadData = enc.encryptData(payloadData, passPhrase)

		return emb.insertPayload(containerData, encryptedPayloadMeta, encryptedPayloadData)

	def extract(self, containerWithPayloadData, passPhrase):
		"""
			Extracts data and metadata both encrypted with a passPhrase from a PNG container's data.

			Parameters:
				containerWithPayloadData (bin) -- PNG binary data with the payload embedded within.
				passPhrase (str) -- password used to decrypt data and metadata embedded in the containerWithPayloadData.

			Returns:
				dict: Data and Metadata embedded in the containerWithPayloadData.
		"""

		emb = Embedder()
		enc = Encrypter()

		encryptedPayload = emb.extractPayload(containerWithPayloadData)

		payload = {}
		payload['meta'] = enc.decryptData(encryptedPayload['filename'], passPhrase)
		payload['data'] = enc.decryptData(encryptedPayload['data'], passPhrase)

		return payload
