from unittest import TestCase
from tilekiln.definition import Definition, wrap_sql, zxy_to_projected, bbox
from tilekiln.definition import tile_length, tile_area
from tilekiln.definition import coordinate_length, coordinate_area


class TestDefinition(TestCase):
    def test_equals(self):
        self.assertEqual(Definition("water", "SELECT *", 0, 4, None),
                         Definition("water", "SELECT *", 0, 4, None))

        self.assertFalse(Definition("water", "SELECT *", 0, 4, None) ==
                         Definition("water", "SELECT *", 0, 2, None))
        self.assertFalse(Definition("water", "SELECT *", 1, 4, None) ==
                         Definition("water", "SELECT *", 0, 4, None))
        self.assertFalse(Definition("water", "SELECT *", 0, 4, None) ==
                         Definition("water", "SELECT 1", 0, 4, None))
        self.assertFalse(Definition("water", "SELECT *", 0, 4, None) ==
                         Definition("land", "SELECT *", 0, 4, None))
        self.assertFalse(Definition("water", "SELECT *", 0, 4, 1024) ==
                         Definition("water", "SELECT *", 0, 4, 256))

    def test_wrap(self):
        self.assertEqual(wrap_sql("select", "layerid", 4096),
                         ('''WITH mvtgeom AS\n'''
                          '''(\n'''
                          '''select\n'''
                          ''')\n'''
                          '''SELECT ST_AsMVT(mvtgeom.*, 'layerid', '''
                          '''4096, 'way', NULL)\n'''
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

    def test_tile_length(self):
        self.assertEqual(tile_length(0), 40075016.68)
        self.assertEqual(tile_length(1), 20037508.34)

    def test_coordinate_length(self):
        self.assertEqual(coordinate_length(0, 256), 156543.03390625)
        self.assertEqual(coordinate_length(0, 1024), 39135.7584765625)
        self.assertEqual(coordinate_length(1, 256), 78271.516953125)
        self.assertEqual(coordinate_length(1, 1024), 19567.87923828125)

    def test_tile_area(self):
        self.assertEqual(tile_area(0), 1606006961902278.2)
        self.assertEqual(tile_area(1), 401501740475569.56)

    def test_coordinate_area(self):
        self.assertEqual(coordinate_area(0, 256), 24505721464.573338)
        self.assertEqual(coordinate_area(0, 1024), 1531607591.5358336)
        self.assertEqual(coordinate_area(1, 256), 6126430366.143334)
        self.assertEqual(coordinate_area(1, 1024), 382901897.8839584)

    def test_bbox(self):
        self.assertEqual(bbox(0, 0, 0),
                         "ST_MakeEnvelope(-20037508.34, -20037508.34, "
                         "20037508.34, 20037508.34, 3857)")
        self.assertEqual(bbox(1, 0, 0),
                         "ST_MakeEnvelope(-20037508.34, 0.0, "
                         "0.0, 20037508.34, 3857)")

    def test_rendering(self):
        d = Definition("water", "zoom: {{zoom}}, x: {{x}}, y: {{y}}",
                       0, 4, None)
        self.assertEqual(d.render_sql((3, 2, 1)),
                         wrap_sql("zoom: 3, x: 2, y: 1", "water", 4096))
        d = Definition("water", "bbox: {{bbox}}", 0, 4, None)
        self.assertEqual(d.render_sql((3, 2, 1)),
                         wrap_sql("bbox: " + bbox(3, 2, 1), "water", 4096))

        d = Definition("water", "length: {{tile_length}}", 0, 4, None)
        self.assertEqual(d.render_sql((1, 0, 0)),
                         wrap_sql("length: " + str(tile_length(1)),
                                  "water", 4096))

        d = Definition("water", "area: {{tile_area}}", 0, 4, None)
        self.assertEqual(d.render_sql((1, 0, 0)),
                         wrap_sql("area: " + str(tile_area(1)), "water", 4096))

        d = Definition("water", "extent: {{extent}}", 0, 4, 1024)
        self.assertEqual(d.render_sql((1, 0, 0)),
                         wrap_sql("extent: 1024", "water", 1024))

        d = Definition("water", "coordinate_length: {{coordinate_length}}",
                       0, 4, None)
        self.assertEqual(d.render_sql((1, 0, 0)),
                         wrap_sql("coordinate_length: " +
                                  str(coordinate_length(1, 4096)), "water",
                                  4096))

        d = Definition("water", "coordinate_area: {{coordinate_area}}",
                       0, 4, None)
        self.assertEqual(d.render_sql((1, 0, 0)),
                         wrap_sql("coordinate_area: " +
                                  str(coordinate_area(1, 4096)), "water",
                                  4096))
