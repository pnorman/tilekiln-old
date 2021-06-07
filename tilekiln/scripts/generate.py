import click
import fs.osfs
import mercantile

import tilekiln.config
import tilekiln.kiln
import os
import multiprocessing
import sys


@click.group()
def cli():
    pass


@cli.command()
@click.argument('config', type=click.Path(exists=True))
@click.argument('storage')
@click.option('-d', '--dbname')
@click.option('-h', '--host')
@click.option('-p', '--port')
@click.option('-U', '--username')
@click.option('-c', '--connections', type=click.INT,
              default=multiprocessing.cpu_count())
@click.option('-s', '--chunk-size', type=click.INT)
@click.option('-z', '--min-zoom', type=click.INT)
@click.option('-Z', '--max-zoom', type=click.INT)
@click.option('--bbox', 'bbox', default='-180,-90,180,90')
def area(config, storage, dbname, host, port, username, connections,
         chunk_size, min_zoom, max_zoom, bbox):
    '''Generates tiles for an area'''
    # Get the directory the config is in
    full_path = os.path.join(os.getcwd(), config)
    root_path = os.path.dirname(full_path)
    config_path = os.path.relpath(full_path, root_path)

    filesystem = fs.osfs.OSFS(root_path)

    config = tilekiln.config.Config(filesystem.open(config_path).read(),
                                    filesystem)
    dbinfo = {"dbname": dbname, "host": host, "port": port,
              "username": username}

    min_zoom = min_zoom or config.minzoom
    max_zoom = max_zoom or config.maxzoom
    zoom_levels = [z for z in range(min_zoom, max_zoom + 1)]

    bounding_box = tuple(map(float, bbox.split(',')))
    if len(bounding_box) != 4:
        raise ValueError(f'Provided bounding box: "{bbox}" is invalid. It should have 4 elements separated by commas.')
    if bounding_box[0] < -180 or bounding_box[0] > 180 or bounding_box[2] < -180 or bounding_box[2] > 180:
        raise ValueError('Longitude cannot be lower than -180 or higher than 180.')
    if bounding_box[1] < -90 or bounding_box[1] > 90 or bounding_box[3] < -90 or bounding_box[3] > 90:
        raise ValueError('Latitude cannot be lower than -90 or higher than 90.')

    tiles = [(tile.z, tile.x, tile.y) for tile in mercantile.tiles(*bounding_box, zoom_levels)]

    # Apply some heuristics to guess a chunk size
    if chunk_size is None:
        chunk_size = int(min(max(len(tiles)/(2*connections), 10), 50000))

    kiln = tilekiln.kiln.Kiln(config, dbinfo, storage)
    kiln.generate_tiles(tiles, connections, chunk_size)


@cli.command()
@click.argument('config', type=click.Path(exists=True))
@click.argument('storage')
@click.option('-d', '--dbname')
@click.option('-h', '--host')
@click.option('-p', '--port')
@click.option('-U', '--username')
@click.option('-c', '--connections', type=click.INT,
              default=multiprocessing.cpu_count())
@click.option('-s', '--chunk-size', type=click.INT)
def tiles(config, storage, dbname, host, port, username, connections,
          chunk_size):
    '''Generate a list of tiles

    Feed the tiles in on stdin and send an EOF to start generation
    '''
    # Get the directory the config is in
    full_path = os.path.join(os.getcwd(), config)
    root_path = os.path.dirname(full_path)
    config_path = os.path.relpath(full_path, root_path)

    filesystem = fs.osfs.OSFS(root_path)

    config = tilekiln.config.Config(filesystem.open(config_path).read(),
                                    filesystem)
    dbinfo = {"dbname": dbname, "host": host, "port": port,
              "username": username}

    tiles = [tuple(int(coord) for coord in line.strip().split('/', 3))
             for line in sys.stdin.readlines() if line.strip() != '']

    if chunk_size is None:
        chunk_size = int(min(max(len(tiles)/(2*connections), 10), 50000))

    kiln = tilekiln.kiln.Kiln(config, dbinfo, storage)
    kiln.generate_tiles(tiles, connections, chunk_size)
