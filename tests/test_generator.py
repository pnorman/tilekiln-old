from unittest import TestCase
from unittest.mock import patch
from tilekiln.generator import Generator
from tilekiln.layer import Layer
from fs.memoryfs import MemoryFS


class MockDB:
    def generate_tilelayer(self, definition, tile):
        return b"result"


class TestGenerator(TestCase):
    def test_constructor(self):
        # TODO: Construct a layers object

        fs = MemoryFS()
        fs.writetext('1.sql', 'select 1')
        fs.writetext('2.sql', 'select 2')
        layers = [Layer("water",
                        {"fields": {},
                         "description": "Waterbody and ocean areas",
                         "sql": [{"minzoom": 0, "maxzoom": 4, "file": "1.sql"},
                                 {"minzoom": 5, "maxzoom": 8, "file": "2.sql"}]
                         }, fs)]
        gen = Generator("v1", layers, {"port": 1234}, "dir")

        self.assertEqual(gen.id, "v1")
        self.assertEqual(gen.layers, layers)
        self.assertEqual(gen.dbconn, {"port": 1234})
        self.assertEqual(gen.storage_location, "dir")

    @patch("tilekiln.database.Database")
    @patch("psycopg2.connect")
    @patch("fs.open_fs")
    def test_write_tiles(self, mock_open, mock_connect, mock_db):
        fs = MemoryFS()
        fs.writetext('1.sql', 'select 1')
        layers = [Layer("water",
                        {"fields": {},
                         "description": "Waterbody and ocean areas",
                         "sql": [{"minzoom": 0, "maxzoom": 4, "file": "1.sql"}]
                         }, fs)]

        out_fs = MemoryFS()

        mock_open.return_value = out_fs
        mock_connect.return_value = None
        mock_db.return_value = MockDB()

        gen = Generator("v1", layers, {"port": 1234}, "storage")

        gen.write_tiles([(0, 0, 0)])

        self.assertEqual(out_fs.openbin("v1/0/0/0.mvt").read(), b"result")
