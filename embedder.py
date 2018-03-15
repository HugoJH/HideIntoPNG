from shutil import copyfile
from os import SEEK_END, SEEK_SET, SEEK_CUR
from os.path import basename
from struct import pack, unpack
from binascii import crc32


class Embedder:

    FILEPOS_BEFORE_ENDCHUNK = -12
    META_CHUNK_TYPE = "meTa".encode('utf-8')
    CONTENT_CHUNK_TYPE = "teMa".encode('utf-8')
    IEND_CHUNK_TYPE = 'IEND'.encode('utf-8')
    SIGNATURE_LENGTH = 8
    CHUNK_SIZE_LENGTH = 4
    CHUNK_TYPE_LENGTH = 4
    CHUNK_CRC_LENGTH = 4
    extraction_index = 0

    def insertPayload(self, containerData, payloadMetaData, payloadData):
        result = containerData[:self.FILEPOS_BEFORE_ENDCHUNK] + self._create_chunk(self.META_CHUNK_TYPE, payloadMetaData)
        result += self._create_chunk(self.CONTENT_CHUNK_TYPE, payloadData)

        result += self._create_chunk(self.IEND_CHUNK_TYPE, '')
        return result


    def _create_chunk (self, chunk_type_bytes, chunk_data_bytes):
      chunk_crc = self._create_chunk_crc(chunk_type_bytes, chunk_data_bytes)
      chunk_content = bytearray(pack('!i', len(chunk_data_bytes)))
      chunk_content.extend(chunk_type_bytes)
      chunk_content.extend(chunk_data_bytes)
      chunk_content.extend(chunk_crc)
      return chunk_content

    def _create_chunk_crc(self, chunk_type_bytes, chunk_data_bytes):
        bytes_for_crc = bytearray()
        bytes_for_crc.extend(chunk_type_bytes)
        bytes_for_crc.extend(chunk_data_bytes)
        return pack('!I', (crc32(bytes_for_crc) & 0xffffffff))

    def extractPayload(self, containerData):
        self._skip_signature(containerData)
        payload = {}

        while True:
            chunkSize = self._read_chunk_size(containerData)
            chunkType = self._read_chunk_type(containerData)

            if ((chunkType != self.META_CHUNK_TYPE) and
                (chunkType != self.IEND_CHUNK_TYPE)):
                self._skip_to_next_chunk(chunkSize)
            elif chunkType == self.META_CHUNK_TYPE:
                meta_chunk_bytes = self._read_chunk_content(containerData, chunkSize)
                self._skip_crc()
                chunkSize = self._read_chunk_size(containerData)
                chunkType = self._read_chunk_type(containerData)
                content_chunk_bytes = self._read_chunk_content(containerData, chunkSize)
                payload['filename'] = meta_chunk_bytes
                payload['data'] = content_chunk_bytes
                break
            elif chunkType == self.IEND_CHUNK_TYPE:
                return "ERROR"
        return payload

    def _skip_signature(self, data):
        self.extraction_index += self.SIGNATURE_LENGTH

    def _skip_to_next_chunk(self, chunk_size):
        self.extraction_index += chunk_size
        self._skip_crc()

    def _skip_crc(self):
        self.extraction_index += self.CHUNK_CRC_LENGTH

    def _read_chunk_size(self, data):
        chunk_size = unpack("!i", data[self.extraction_index:self.extraction_index + self.CHUNK_SIZE_LENGTH])[0]
        self.extraction_index += self.CHUNK_SIZE_LENGTH
        return chunk_size

    def _read_chunk_type(self, data):
        chunkType = data[self.extraction_index:self.extraction_index + self.CHUNK_TYPE_LENGTH]
        self.extraction_index += self.CHUNK_TYPE_LENGTH
        return chunkType

    def _read_chunk_content(self, data, chunkSize):
        chunkContent = data[self.extraction_index:self.extraction_index + chunkSize]
        self.extraction_index += chunkSize
        return chunkContent