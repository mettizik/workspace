from unittest import TestCase
from workspace.bindata.struct_unpack import *

def make_numeric_field(field_name='sample', _bytes_count=1):
    return Struct.Field(field_name, Struct.Field.TYPE_NUMBER, size=_bytes_count)

def unpack_and_test_numeric_field(self, numb, bytes_count=1):    
    field = make_numeric_field(_bytes_count=bytes_count)
    data = io.BytesIO(numb.to_bytes(bytes_count, SystemByteorder))
    unpack_field(field, data)
    self.assertEqual(field.value, numb)
    self.assertEqual(field.raw_data, data.getvalue())
    return field

class struct_processor(TestCase):
    def test_field_unpack_can_unpack_integer_one(self):
        unpack_and_test_numeric_field(self, 1)

    def test_field_unpack_can_unpack_integer_ten(self):
        unpack_and_test_numeric_field(self, 10)

    def test_field_unpack_can_unpack_integer_255(self):
        unpack_and_test_numeric_field(self, 255)

    def test_field_unpack_can_unpack_integer_256(self):
        unpack_and_test_numeric_field(self, 256, 2)

    def test_field_unpack_can_unpack_integer_100500(self):
        field = unpack_and_test_numeric_field(self, 100500, 3)
        self.assertEqual(b'\x94\x88\x01', field.raw_data)

    def test_struct_unpack_can_unpack_sctruct_with_single_numeric_field(self):
        field = make_numeric_field('field')
        raw_data = int(1).to_bytes(1, SystemByteorder)
        struct = Struct('sample', [field]).Unpack(
            io.BytesIO(raw_data))
        self.assertEqual(1, struct['field']['value'])
        self.assertEqual(raw_data, struct['field']['raw_data'])
