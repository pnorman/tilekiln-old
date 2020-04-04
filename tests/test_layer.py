from unittest import TestCase
from unittest.mock import Mock
from tilekiln.layer import Layer
from tilekiln.definition import Definition
from tilekiln.database import Database
from fs.memoryfs import MemoryFS


class TestLayer(TestCase):
    def test_equals(self):
        fs1 = MemoryFS()
        fs1.writetext('foo.sql', 'select 1')
        fs2 = MemoryFS()
        fs2.writetext('foo.sql', 'select 2')
        fs2.writetext('bar.sql', 'select 1')

        self.assertEqual(Layer("water",
                               {"fields": {"water": "type of water"},
                                "description": "Waterbody and ocean areas",
                                "sql": [{"minzoom": 0, "maxzoom": 4,
                                         "file": "foo.sql"}]
                                }, fs1),
                         Layer("water",
                               {"fields": {"water": "type of water"},
                                "description": "Waterbody and ocean areas",
                                "sql": [{"minzoom": 0, "maxzoom": 4,
                                         "file": "foo.sql"}]
                                }, fs1))

        # Only file contents should matter
        self.assertEqual(Layer("water",
                               {"fields": {"water": "type of water"},
                                "description": "Waterbody and ocean areas",
                                "sql": [{"minzoom": 0, "maxzoom": 4,
                                         "file": "foo.sql"}]
                                }, fs1),
                         Layer("water",
                               {"fields": {"water": "type of water"},
                                "description": "Waterbody and ocean areas",
                                "sql": [{"minzoom": 0, "maxzoom": 4,
                                         "file": "bar.sql"}]
                                }, fs2))

        # id
        self.assertFalse(Layer("land",
                               {"fields": {"water": "type of water"},
                                "description": "Waterbody and ocean areas",
                                "sql": [{"minzoom": 0, "maxzoom": 4,
                                         "file": "foo.sql"}]
                                }, fs1) ==
                         Layer("water",
                               {"fields": {"water": "type of water"},
                                "description": "Waterbody and ocean areas",
                                "sql": [{"minzoom": 0, "maxzoom": 4,
                                         "file": "foo.sql"}]
                                }, fs1))

        # fields
        self.assertFalse(Layer("water",
                               {"fields": {"water": "type of land"},
                                "description": "Waterbody and ocean areas",
                                "sql": [{"minzoom": 0, "maxzoom": 4,
                                         "file": "foo.sql"}]
                                }, fs1) ==
                         Layer("water",
                               {"fields": {"water": "type of water"},
                                "description": "Waterbody and ocean areas",
                                "sql": [{"minzoom": 0, "maxzoom": 4,
                                         "file": "foo.sql"}]
                                }, fs1))
        self.assertFalse(Layer("water",
                               {"fields": {"land": "type of water"},
                                "description": "Waterbody and ocean areas",
                                "sql": [{"minzoom": 0, "maxzoom": 4,
                                         "file": "foo.sql"}]
                                }, fs1) ==
                         Layer("water",
                               {"fields": {"water": "type of water"},
                                "description": "Waterbody and ocean areas",
                                "sql": [{"minzoom": 0, "maxzoom": 4,
                                         "file": "foo.sql"}]
                                }, fs1))

        # zooms
        self.assertFalse(Layer("water",
                               {"fields": {"water": "type of water"},
                                "description": "Waterbody and ocean areas",
                                "sql": [{"minzoom": 0, "maxzoom": 2,
                                         "file": "foo.sql"}]
                                }, fs1) ==
                         Layer("water",
                               {"fields": {"water": "type of water"},
                                "description": "Waterbody and ocean areas",
                                "sql": [{"minzoom": 0, "maxzoom": 4,
                                         "file": "foo.sql"}]
                                }, fs1))
        self.assertFalse(Layer("water",
                               {"fields": {"water": "type of water"},
                                "description": "Waterbody and ocean areas",
                                "sql": [{"minzoom": 2, "maxzoom": 4,
                                         "file": "foo.sql"}]
                                }, fs1) ==
                         Layer("water",
                               {"fields": {"water": "type of water"},
                                "description": "Waterbody and ocean areas",
                                "sql": [{"minzoom": 0, "maxzoom": 4,
                                         "file": "foo.sql"}]
                                }, fs1))

        # sql
        self.assertFalse(Layer("water",
                               {"fields": {"water": "type of water"},
                                "description": "Waterbody and ocean areas",
                                "sql": [{"minzoom": 0, "maxzoom": 4,
                                         "file": "foo.sql"}]
                                }, fs1) ==
                         Layer("water",
                               {"fields": {"water": "type of water"},
                                "description": "Waterbody and ocean areas",
                                "sql": [{"minzoom": 0, "maxzoom": 4,
                                         "file": "foo.sql"}]
                                }, fs2))

    def test_definition_for_zoom(self):
        fs = MemoryFS()
        fs.writetext('1.sql', 'select 1')
        fs.writetext('2.sql', 'select 2')
        layer = Layer("water",
                      {"fields": {},
                       "description": "Waterbody and ocean areas",
                       "sql": [{"minzoom": 0, "maxzoom": 4, "file": "1.sql"},
                               {"minzoom": 5, "maxzoom": 8, "file": "2.sql"}]
                       }, fs)

        for i in range(0, 5):
            self.assertEqual(layer.definition_for_zoom(i),
                             Definition("water", "select 1", 0, 4, None))

        for i in range(5, 9):
            self.assertEqual(layer.definition_for_zoom(i),
                             Definition("water", "select 2", 5, 8, None))

        self.assertIsNone(layer.definition_for_zoom(9), None)

    def test_fields(self):
        fs = MemoryFS()
        fs.writetext('1.sql', 'select 1')
        layer = Layer("water",
                      {"fields": {"water": "type of water"},
                       "description": "Waterbody and ocean areas",
                       "sql": [{"minzoom": 0, "maxzoom": 4, "file": "1.sql"}]
                       }, fs)

        self.assertEqual(layer.fields["water"], "type of water")

    def test_render_tile(self):
        fs = MemoryFS()
        fs.writetext('1.sql', 'select 1')
        fs.writetext('2.sql', 'select 2')
        layer = Layer("water",
                      {"fields": {},
                       "description": "Waterbody and ocean areas",
                       "sql": [{"minzoom": 0, "maxzoom": 4, "file": "1.sql"},
                               {"minzoom": 5, "maxzoom": 8, "file": "2.sql"}]
                       }, fs)

        db = Database(Mock())
        db.generate_tilelayer = Mock(return_value=b'foo')

        layer.render_tile((0, 0, 0), db)
        db.generate_tilelayer.assert_called_with(layer.definition_for_zoom(0),
                                                 (0, 0, 0))
