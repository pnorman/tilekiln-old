import yaml
import tilekiln.layer


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
