from unittest import TestCase
from fs.memoryfs import MemoryFS
from tilekiln.config import Config
from tilekiln.layer import Layer
import yaml


class TestConfig(TestCase):
    def test_properties(self):
        with MemoryFS() as fs:
            c = Config('''{"metadata": {"id":"v1"}}''', fs)
            self.assertEqual(c.id, "v1")
            self.assertEqual(c.name, None)
            self.assertEqual(c.description, None)
            self.assertEqual(c.attribution, None)
            self.assertEqual(c.version, None)
            self.assertEqual(c.bounds, None)
            self.assertEqual(c.center, None)

        with MemoryFS() as fs:
            c_str = ('''{"metadata": {"id":"v1", "name": "name", '''
                     '''"description":"description", '''
                     '''"attribution":"attribution", "version": "1.0.0",'''
                     '''"bounds": [-180, -85, 180, 85], "center": [0, 0]},'''
                     '''"vector_layers": {"building":{'''
                     '''"description": "buildings",'''
                     '''"fields":{}}}}''')

            # Check the test is valid yaml to save debugging
            yaml.safe_load(c_str)
            c = Config(c_str, fs)
            self.assertEqual(c.id, "v1")
            self.assertEqual(c.name, "name")
            self.assertEqual(c.description, "description")
            self.assertEqual(c.attribution, "attribution")
            self.assertEqual(c.version, "1.0.0")
            self.assertEqual(c.bounds, [-180, -85, 180, 85])
            self.assertEqual(c.center, [0, 0])
            self.assertEqual(len(c.layers), 1)
            self.assertEqual(c.layers[0],
                             Layer("building", {"description": "buildings",
                                                "fields": {}}, fs))
