from unittest import TestCase
from fs.memoryfs import MemoryFS
from tilekiln.config import Config
from tilekiln.layer import Layer
import yaml
import json

sample_config = '''
metadata:
  id: v1 # Required, used internally by Tilekiln
  bounds: [-180, -85.05112877980659, 180, 85.0511287798066 ]
  name: name for tilejson, optional
  description: description for tilejson, optional
  version: version for tilejson, optional
  attribution: attribution for tilejson, optional
  center: [0, 0] # center for tilejson, optional
vector_layers:
  water:
    fields:
      water: Type of water
    description: Waterbody and ocean areas
    sql:
    - minzoom: 0
      maxzoom: 8
      file: water.sql.jinja2
  admin:
    fields:
      admin_level: Level of admin boundary
    description: Administrative boundaries
    sql:
    - minzoom: 1 # Must not overlap with other templates
      maxzoom: 3
      file: ne-admin.sql.jinja2
    - minzoom: 4 # Must not overlap with other templates
      maxzoom: 10
      file: admin.sql.jinja2
  country_names:
    fields:
      name: Name of country
      area: Area of country
    description: Points for country names
    sql:
    - minzoom: 3
      maxzoom: 14
      file: country.sql.jinja2
'''


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

    def test_zooms(self):
        with MemoryFS() as fs:
            fs.writetext("water.sql.jinja2", "select 1")
            fs.writetext("ne-admin.sql.jinja2", "select 2")
            fs.writetext("admin.sql.jinja2", "select 3")
            fs.writetext("country.sql.jinja2", "select 4")
            config = Config(sample_config, fs)
            self.assertEqual(config.minzoom, 0)
            self.assertEqual(config.maxzoom, 14)

    def test_tilejson(self):
        with MemoryFS() as fs:
            tj = json.loads(Config('''{"metadata": {"id":"v1"}}''', fs)
                            .tilejson("http://localhost/{id}/{z}/{x}/{y}.mvt"))

            self.assertEqual(tj["tilejson"], "2.2.0")
            self.assertEqual(tj["format"], "pbf")
            self.assertEqual(tj["scheme"], "xyz")
            self.assertEqual(tj["tiles"],
                             ["http://localhost/v1/{z}/{x}/{y}.mvt"])

        with MemoryFS() as fs:
            fs.writetext("water.sql.jinja2", "select 1")
            fs.writetext("ne-admin.sql.jinja2", "select 2")
            fs.writetext("admin.sql.jinja2", "select 3")
            fs.writetext("country.sql.jinja2", "select 4")
            tj = json.loads(Config(sample_config, fs)
                            .tilejson("http://localhost/{id}/{z}/{x}/{y}.mvt"))

            self.assertEqual(tj["name"], "name for tilejson, optional")
            self.assertEqual(tj["description"],
                             "description for tilejson, optional")
            self.assertEqual(tj["attribution"],
                             "attribution for tilejson, optional")
            self.assertEqual(tj["version"], "version for tilejson, optional")
            self.assertEqual(tj["bounds"],
                             [-180, -85.05112877980659, 180, 85.0511287798066])
            self.assertEqual(tj["center"], [0, 0])

            self.assertEqual(tj["minzoom"], 0)
            self.assertEqual(tj["maxzoom"], 14)

            # tilejsons have a list of layers you need to iterate through
            water = {}
            admin = {}
            country_names = {}

            self.assertEqual(len(tj["vector_layers"]), 3)
            for l in tj["vector_layers"]:
                if l["id"] == "water":
                    water = l
                elif l["id"] == "admin":
                    admin = l
                elif l["id"] == "country_names":
                    country_names = l

            self.assertEqual(water["id"], "water")
            self.assertEqual(water["description"], "Waterbody and ocean areas")
            self.assertEqual(water["minzoom"], 0)
            self.assertEqual(water["maxzoom"], 8)
            self.assertEqual(water["fields"],
                             {"water": "Type of water"})

            self.assertEqual(admin["id"], "admin")
            self.assertEqual(admin["description"], "Administrative boundaries")
            self.assertEqual(admin["minzoom"], 1)
            self.assertEqual(admin["maxzoom"], 10)
            self.assertEqual(admin["fields"],
                             {"admin_level": "Level of admin boundary"})

            self.assertEqual(country_names["id"], "country_names")
            self.assertEqual(country_names["description"],
                             "Points for country names")
            self.assertEqual(country_names["minzoom"], 3)
            self.assertEqual(country_names["maxzoom"], 14)
            self.assertEqual(country_names["fields"],
                             {"area": "Area of country",
                              "name": "Name of country"})
