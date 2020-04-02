from unittest import TestCase
from tilekiln.definition import Definition, wrap_sql, zxy_to_projected, bbox


class TestDefinition(TestCase):
    def test_equals(self):
        self.assertEqual(Definition("water", "SELECT *", 0, 4),
                         Definition("water", "SELECT *", 0, 4))

        self.assertFalse(Definition("water", "SELECT *", 0, 4) ==
                         Definition("water", "SELECT *", 0, 2))
        self.assertFalse(Definition("water", "SELECT *", 1, 4) ==
                         Definition("water", "SELECT *", 0, 4))
        self.assertFalse(Definition("water", "SELECT *", 0, 4) ==
                         Definition("water", "SELECT 1", 0, 4))
        self.assertFalse(Definition("water", "SELECT *", 0, 4) ==
                         Definition("land", "SELECT *", 0, 4))

    def test_wrap(self):
        self.assertEqual(wrap_sql("select", "layerid"),
                         ('''WITH mvtgeom AS\n'''
                          '''(\n'''
                          '''select\n'''
                          ''')\n'''
                          '''SELECT ST_AsMVT(mvtgeom.*, 'layerid', 4096, '''
                          ''''way', NULL)\n'''
                          '''FROM mvtgeom;'''))

    def test_tile_to_projected(self):
        HALF_WORLD = 20037508.34
        self.assertEqual(zxy_to_projected(0, 0, 0), [-HALF_WORLD, HALF_WORLD])
        self.assertEqual(zxy_to_projected(1, 0, 0), [-HALF_WORLD, HALF_WORLD])
        self.assertEqual(zxy_to_projected(2, 0, 0), [-HALF_WORLD, HALF_WORLD])

        self.assertEqual(zxy_to_projected(0, 0, 1), [-HALF_WORLD, -HALF_WORLD])
        self.assertEqual(zxy_to_projected(0, 1, 0), [HALF_WORLD, HALF_WORLD])
        self.assertEqual(zxy_to_projected(0, 1, 1), [HALF_WORLD, -HALF_WORLD])

        self.assertEqual(zxy_to_projected(1, 1, 1), [0, 0])

    def test_bbox(self):
        self.assertEqual(bbox(0, 0, 0),
                         "ST_MakeEnvelope(-20037508.34, -20037508.34, "
                         "20037508.34, 20037508.34, 3857)")
        self.assertEqual(bbox(1, 0, 0),
                         "ST_MakeEnvelope(-20037508.34, 0.0, "
                         "0.0, 20037508.34, 3857)")

    def test_rendering(self):
        d = Definition("water", "zoom: {{zoom}}, x: {{x}}, y: {{y}}", 0, 4)
        self.assertEqual(d.render_sql((3, 2, 1)),
                         wrap_sql("zoom: 3, x: 2, y: 1", "water"))
        d = Definition("water", "bbox: {{bbox}}", 0, 4)
        self.assertEqual(d.render_sql((3, 2, 1)),
                         wrap_sql("bbox: " + bbox(3, 2, 1), "water"))
