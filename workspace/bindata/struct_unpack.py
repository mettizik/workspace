import io
from sys import byteorder as SystemByteorder
class Struct:
    """
class that represents a binary structure
    """

    class Field:
        """
    class that represents a binary structure
        """

        TYPE_NUMBER = 0
        TYPE_STRING = 1
        TYPE_BYTES  = 2

        def __init__(self, field_name: str, field_type: int, size=None):
            """
        create a field of a structure with given name, type and size
            """
            self.name = field_name
            self.type = field_type
            self.size = size
            self.value = None
            self.raw_data = None

    def __init__(self, name:str, fields:list):
        """
    Create a structure, with provided names and fields
        """
        self._name = name
        self._fields = fields

def unpack_field(field: Struct.Field, bindata:io.RawIOBase):
    raw_data = bindata.read(field.size)
    field.value = int.from_bytes(raw_data, byteorder=SystemByteorder)
    field.raw_data = raw_data
