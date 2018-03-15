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

    def insertPayload(self, containerData, payloadMeta, payloadData):
        result = containerData[:self.FILEPOS_BEFORE_ENDCHUNK] + self._create_chunk(self.META_CHUNK_TYPE, basename(payloadMeta).encode('utf-8'))
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

    def extractPayload(self, containerFilePath):
      with open(containerFilePath, 'rb+') as containerFileFD:
          self._skip_signature(containerFileFD)
          payload = {}

          while True:
             chunk_size = self._read_chunk_size(containerFileFD)
             chunk_type = self._read_chunk_type(containerFileFD)

             if ((chunk_type != self.META_CHUNK_TYPE) and
                (chunk_type != self.IEND_CHUNK_TYPE)):
                self._skip_to_next_chunk(containerFileFD, chunk_size)
             elif chunk_type == self.META_CHUNK_TYPE:
                meta_chunk_bytes = self._read_chunk_content(containerFileFD, chunk_size)
                self._skip_crc(containerFileFD)
                chunk_size = self._read_chunk_size(containerFileFD)
                chunk_type = self._read_chunk_type(containerFileFD)
                content_chunk_bytes = self._read_chunk_content(containerFileFD, chunk_size)
                payload['filename'] = meta_chunk_bytes
                payload['data'] = content_chunk_bytes
                break
             elif chunk_type == self.IEND_CHUNK_TYPE:
                return "ERROR"

      return payload

    def _skip_signature(self, file):
      file.seek(self.SIGNATURE_LENGTH, SEEK_SET)

    def _skip_to_next_chunk(self, file, chunk_size):
        file.seek(chunk_size, SEEK_CUR)
        self._skip_crc(file)

    def _skip_crc(self, file):
        file.seek(self.CHUNK_CRC_LENGTH, SEEK_CUR)

    def _read_chunk_size(self, file):
        return unpack("!i", file.read(self.CHUNK_SIZE_LENGTH))[0]

    def _read_chunk_type(self, file):
        return file.read(self.CHUNK_TYPE_LENGTH)

    def _read_chunk_content(self, file, chunk_size):
        return file.read(chunk_size)