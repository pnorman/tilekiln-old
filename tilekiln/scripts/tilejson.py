import click
import fs.osfs
import tilekiln.config
import tilekiln.kiln
import os


@click.command()
@click.argument('config', type=click.Path(exists=True))
@click.argument('url', default='http://localhost/{id}/{z}/{x}/{y}.mvt')
def cli(config, url):
    # Get the directory the config is in
    # TODO: Reduce duplication between this and tilejson-generate
    full_path = os.path.join(os.getcwd(), config)
    root_path = os.path.dirname(full_path)
    config_path = os.path.relpath(full_path, root_path)

    filesystem = fs.osfs.OSFS(root_path)

    config = tilekiln.config.Config(filesystem.open(config_path).read(),
                                    filesystem)
    print(config.tilejson(url))
