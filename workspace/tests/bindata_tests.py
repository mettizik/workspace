from unittest import TestCase
from workspace.bindata.struct_unpack import *


def make_bytes_field(field_name='sample', _bytes_count=0):
    return Struct.Field(field_name, Struct.Field.TYPE_BYTES, size=_bytes_count)

def make_string_field(field_name='sample', _bytes_count=0):
    return Struct.Field(field_name, Struct.Field.TYPE_STRING, size=_bytes_count)

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
    
    def test_struct_unpack_can_unpack_one_numeric_field_and_skips_unused_dat(self):
        raw_data = bytes([0x01, 0x02, 0x03])
        struct = Struct('sample', [
            make_numeric_field('field1')
        ]).Unpack(
            io.BytesIO(raw_data))
        self.assertEqual(1, struct['field1']['value'])
        self.assertEqual(b'\x01', struct['field1']['raw_data'])
        self.assertEqual(1, len(struct))

    def test_field_unpack_can_unpack_string_hello(self):
        raw_data = b'hello'
        field = make_string_field(_bytes_count=len(raw_data))
        field.Unpack(io.BytesIO(raw_data))
        self.assertEqual(raw_data.decode(), field.Pretty())
        self.assertEqual(raw_data, field.Raw())

    def test_field_unpack_throws_on_length_less_than_provided(self):
        raw_data = b'hell'
        field = make_string_field(_bytes_count=5)
        with self.assertRaises(BufferError):
            field.Unpack(io.BytesIO(raw_data))

    def test_struct_unpack_can_unpack_string_hello_into_string_and_numeric_fields(self):
        raw_data = b'hello'

        struct = Struct('sample', [
            make_string_field('str', _bytes_count=len(raw_data) - 1),
            make_numeric_field('num')
        ]).Unpack(
            io.BytesIO(raw_data))

        self.assertEqual('hell', struct['str']['value'])
        self.assertEqual(raw_data[:-1], struct['str']['raw_data'])
        self.assertEqual(0x6f, struct['num']['value'])
        self.assertEqual(raw_data[-1:], struct['num']['raw_data'])
    
    def test_field_unpack_can_unpack_bytes_hello(self):
        raw_data = b'hello'
        field = make_bytes_field(_bytes_count=len(raw_data))
        field.Unpack(io.BytesIO(raw_data))
        self.assertEqual('68656c6c6f', field.Pretty())
        self.assertEqual(raw_data, field.Raw())

    def test_struct_unpack_can_unpack_string_hellohello_into_string_and_numeric_fields(self):
        raw_data = b'hellohello'

        struct = Struct('sample', [
            make_string_field('str', _bytes_count=len(raw_data) - 6),
            make_numeric_field('num'),
            make_bytes_field('hex', 5)
        ]).Unpack(
            io.BytesIO(raw_data))

        self.assertEqual('hell', struct['str']['value'])
        self.assertEqual(raw_data[:-6], struct['str']['raw_data'])
        self.assertEqual(0x6f, struct['num']['value'])
        self.assertEqual(raw_data[-6:-5], struct['num']['raw_data'])
        self.assertEqual('68656c6c6f', struct['hex']['value'])
        self.assertEqual(raw_data[-5:], struct['hex']['raw_data'])
