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

        def from_text(text_line: str, **kwargs):
            """
        Build a field from text definition. Line format should match following line:
            TYPE[LENGTH] NAME;
            , where:
                - TYPE - is one of 'number', 'text', 'bytes'
                - LENGTH - is expected length of field in bytes
                - NAME - is name of the field 
            """
            correct_line = ''.join(e for e in text_line.replace(
                ' ', '').replace('\t', '') if e.isprintable())
            if correct_line:
                text_to_type = {
                    'number': Struct.Field.TYPE_NUMBER,
                    'text': Struct.Field.TYPE_STRING,
                    'bytes': Struct.Field.TYPE_BYTES,
                }
                semicolomn_position = correct_line.find(';')
                if semicolomn_position == -1:
                    raise RuntimeError('No semicolumn found in line {}'.format(text_line))
                closing_bracer_position = correct_line.find(']')
                opening_bracer_position = correct_line.find('[')
                type_text = correct_line[:opening_bracer_position]
                field_size = correct_line[opening_bracer_position + 1:closing_bracer_position]
                field_size = int(field_size, base=16 if 'x' in field_size else 10)
                return Struct.Field(
                    field_name=correct_line[closing_bracer_position + 1:semicolomn_position], 
                    field_type=text_to_type[type_text], 
                    size=field_size)

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

    def from_text(struct_name: str, text: io.StringIO, **kwargs):
        """
    Parses a text representation of a structure into Struct object. 
        """
        parsed_fields = [Struct.Field.from_text(
            line) for line in text.readlines()]
        parsed_fields = [f for f in parsed_fields if f is not None]
        return Struct(name=struct_name, fields=parsed_fields, **kwargs)

    def __init__(self, name: str, fields: list):
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
    
    def Name(self):
        """
    Returns structure name
        """
        return self._name

    def Fields(self):
        """
    Returns all fields of structure
        """
        return self._fields
