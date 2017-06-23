from unittest import TestCase
from workspace.bindata.struct_unpack import *

class struct_processor(TestCase):
    def test_smart_unpack_can_unpack_integer(self):
        field = Struct.Field('1', Struct.Field.TYPE_NUMBER, size=1)
        data = io.BytesIO(bytes([1]))
        unpack_field(field, data)
        self.assertEqual(field.value, 1)
        self.assertEqual(field.raw_data, data.getvalue())

