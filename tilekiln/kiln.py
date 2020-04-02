import multiprocessing.pool
import tilekiln.generator


class Kiln:
    ''' Class that makes tiles
    '''
    def __init__(self, config, dbconn, storage_location):
        '''Create the kiln for tiles

        config - Config object
        dbinfo - database connection params
        storage_location - storage location
        connections - number of connections
        '''

        self.config = config
        self.dbconn = dbconn
        self.storage_location = storage_location

    def generate_tiles(self, tiles, connections, chunk_size):
        chunks = [tiles[i * chunk_size:(i+1) * chunk_size]
                  for i in range((len(tiles) + chunk_size - 1) // chunk_size)]

        gen = tilekiln.generator.Generator(self.config.id, self.config.layers,
                                           self.dbconn, self.storage_location)

        with multiprocessing.pool.Pool(connections) as p:
            p.map(gen.write_tiles, chunks)
