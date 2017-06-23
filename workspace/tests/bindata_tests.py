from unittest import TestCase
from workspace.bindata.struct_unpack import smart_unpack

class struct_processor(TestCase):
    def test_smart_unpack_can_unpack_integer(self):
        res = smart_unpack({'struct': [{'type': 'n:1', 'name': '1'}]}, bytes([1]))
        self.assertEqual(res['name'], '1')
        self.assertEqual(res['value'], 1)
        self.assertEqual(res['raw'], bytes([1]))

