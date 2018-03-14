from shutil import copyfile
from os import SEEK_END
from os.path import basename
from struct import pack
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

    def insertPayload(self, containerFilePath, payloadFilePath, resultFilePath):
        copyfile(containerFilePath, resultFilePath)
        with open(resultFilePath, "rb+") as resultfd:
            resultfd.seek(self.FILEPOS_BEFORE_ENDCHUNK, SEEK_END)
            resultfd.write(self._create_chunk(self.META_CHUNK_TYPE, basename(payloadFilePath).encode('utf-8')))
            with open(payloadFilePath, "rb") as payloadfd:
                resultfd.write(self._create_chunk(self.CONTENT_CHUNK_TYPE, payloadfd.read()))
            resultfd.write(self._create_chunk(self.IEND_CHUNK_TYPE, ''))


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

    def extractPayload(self, containerFilePath):
        pass
