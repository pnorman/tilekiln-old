import yaml
import tilekiln.layer
import json


class Config:
    def __init__(self, yaml_string, fs):
        '''Create a config from a yaml string
           Creates a config from the yaml string. Any SQL files referenced
           must be in the filesystem.
        '''
        config = yaml.safe_load(yaml_string)

        # There's a lot of metadata properties, so pull that table out
        md = config["metadata"]
        self.id = md["id"]
        self.name = md.get("name")
        self.description = md.get("description")
        self.attribution = md.get("attribution")
        self.version = md.get("version")
        self.bounds = md.get("bounds")
        self.center = md.get("center")

        self.layers = []
        # Make vector_layers optional. TODO: Reconsider
        for id, l in config.get("vector_layers", {}).items():
            self.layers.append(tilekiln.layer.Layer(id, l, fs))

    @property
    def minzoom(self):
        return min([layer.minzoom for layer in self.layers])

    @property
    def maxzoom(self):
        return max([layer.maxzoom for layer in self.layers])

    def tilejson(self, url):
        '''Returns a tilejson as a string for the config
        '''

        # See https://github.com/mapbox/tilejson-spec/tree/master/2.2.0

        # Work by assembling a dictionary then turning it into json

        # Required properties
        tj = {"tilejson": "2.2.0",
              "format": "pbf",
              "scheme": "xyz",
              "tiles": [url.replace("{id}", self.id)]}

        if self.name is not None:
            tj["name"] = self.name
        if self.description is not None:
            tj["description"] = self.description
        if self.attribution is not None:
            tj["attribution"] = self.attribution
        if self.version is not None:
            tj["version"] = self.version
        if self.bounds is not None:
            tj["bounds"] = self.bounds
        if self.center is not None:
            tj["center"] = self.center

        if len(self.layers) > 0:
            tj["minzoom"] = min([layer.minzoom for layer in self.layers])
            tj["maxzoom"] = max([layer.maxzoom for layer in self.layers])

            tj["vector_layers"] = []
            for layer in self.layers:
                tj_layer = {"id": layer.id}
                if layer.description is not None:
                    tj_layer["description"] = layer.description
                tj_layer["minzoom"] = layer.minzoom
                tj_layer["maxzoom"] = layer.maxzoom

                tj_layer["fields"] = layer.fields

                if layer.geometry_type == set(["polygon"]):
                    tj_layer["geometry_type"] = "polygon"
                elif layer.geometry_type == set(["point"]):
                    tj_layer["geometry_type"] = "point"
                elif layer.geometry_type == set(["line"]):
                    tj_layer["geometry_type"] = "line"
                else:
                    tj_layer["geometry_type"] = "unknown"

                tj["vector_layers"].append(tj_layer)

        return json.dumps(tj, sort_keys=True, indent=4)
