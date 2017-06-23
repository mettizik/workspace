import io
from sys import byteorder as SystemByteorder
from binascii import hexlify

class Struct:
    """
class that represents a binary structure
    """

    class Field:
        """
    class that represents a binary structure
        """

        TYPE_NUMBER = 0

        def PrettyfyNumber(self, raw_data):
            return int.from_bytes(raw_data, byteorder=self._byteorder)

        TYPE_STRING = 1

        def PrettyfyString(self, raw_data):
            return raw_data.decode()

        TYPE_BYTES  = 2

        def PrettyfyBytes(self, raw_data):            
            return hexlify(raw_data).decode()

        def __init__(self, field_name: str, field_type: int, size=None):
            """
        create a field of a structure with given name, type and size
            """
            self._name = field_name
            self._type = field_type
            self._size = size
            self._byteorder = SystemByteorder
            self._decoders = {
                Struct.Field.TYPE_NUMBER: Struct.Field.PrettyfyNumber,
                Struct.Field.TYPE_STRING: Struct.Field.PrettyfyString,
                Struct.Field.TYPE_BYTES: Struct.Field.PrettyfyBytes
            }

            self._value = None
            self._raw_data = None

        def Unpack(self, bindata):
            """
        Unpack binary data as provided in field's description
            """
            raw_data = bindata.read(self._size)
            if len(raw_data) != self._size:
                raise BufferError('Buffer has not enough data to unpack field ({} < {})'.format(len(raw_data), self._size))
            self._raw_data = raw_data
        
        def Pretty(self):
            """
        Returns a pretty-formatted value
            """
            return self._decoders[self._type](self, self._raw_data)
        
        def Raw(self):
            """
        Returns a raw binary data stored in field
            """
            return self._raw_data
        
        def Name(self):
            """
        Returns defined name
            """
            return self._name

    def __init__(self, name:str, fields:list):
        """
    Create a structure, with provided names and fields
        """
        self._name = name
        self._fields = fields

    def Unpack(self, binary_data: io.RawIOBase):
        """
    Unpack binary data as provided structure definition
        """
        retvals = {}
        for field in self._fields:
            field.Unpack(binary_data)
            retvals[field.Name()] = {
                'value': field.Pretty(),
                'raw_data': field.Raw()
            }

        return retvals


