from unittest import TestCase
from workspace.bindata.struct_unpack import *

def make_numeric_field(field_name='sample', _bytes_count=1):
    return Struct.Field(field_name, Struct.Field.TYPE_NUMBER, size=_bytes_count)

def unpack_and_test_numeric_field(self, numb, bytes_count=1):    
    field = make_numeric_field(_bytes_count=bytes_count)
    data = io.BytesIO(numb.to_bytes(bytes_count, SystemByteorder))
    field.Unpack(data)
    self.assertEqual(field.Pretty(), numb)
    self.assertEqual(field.Raw(), data.getvalue())
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
        self.assertEqual(b'\x94\x88\x01', field.Raw())

    def test_struct_unpack_can_unpack_sctruct_with_single_numeric_field(self):
        field = make_numeric_field('field')
        raw_data = int(1).to_bytes(1, SystemByteorder)
        struct = Struct('sample', [field]).Unpack(
            io.BytesIO(raw_data))
        self.assertEqual(1, struct['field']['value'])
        self.assertEqual(raw_data, struct['field']['raw_data'])

    def test_struct_unpack_can_unpack_two_numeric_fields_of_same_size(self):        
        raw_data = bytes([0x01, 0x02])
        struct = Struct('sample', [
            make_numeric_field('field1'),
            make_numeric_field('field2')
        ]).Unpack(
            io.BytesIO(raw_data))
        self.assertEqual(1, struct['field1']['value'])
        self.assertEqual(b'\x01', struct['field1']['raw_data'])
        self.assertEqual(2, struct['field2']['value'])
        self.assertEqual(b'\x02', struct['field2']['raw_data'])

    def test_struct_unpack_can_unpack_two_numeric_fields_of_different_size(self):
        raw_data = bytes([0x01, 0x02, 0x03])
        struct = Struct('sample', [
            make_numeric_field('field1'),
            make_numeric_field('field2', 2)
        ]).Unpack(
            io.BytesIO(raw_data))
        self.assertEqual(1, struct['field1']['value'])
        self.assertEqual(b'\x01', struct['field1']['raw_data'])
        self.assertEqual(0x0302, struct['field2']['value'])
        self.assertEqual(b'\x02\x03', struct['field2']['raw_data'])
