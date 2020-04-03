import psycopg2
import fs
import tilekiln.database


class Generator:
    def __init__(self, id, layers, dbconn, storage_location):
        '''Sets up the generator
           to generate using dbconn as specified in config and write to
           storage
        '''
        self.id = id
        self.layers = layers
        self.dbconn = dbconn
        self.storage_location = storage_location

    def write_tiles(self, tiles):
        ''' Connect to DB & storage and generate & write tiles
        '''
        db = tilekiln.database.Database(psycopg2.connect(**self.dbconn))
        filesystem = fs.open_fs(self.storage_location, create=True)

        for tile in tiles:
            tiledata = b''

            # TODO: Go through layers
            for layer in self.layers:
                layerdata = layer.render_tile(tile, db)
                if layerdata is not None:
                    tiledata += layerdata

            zoom = tile[0]
            x = tile[1]
            y = tile[2]
            output_dir = "{id}/{z}/{x}/".format(id=self.id, z=zoom, x=x)
            filesystem.makedirs(output_dir, recreate=True)
            output_path = output_dir + "{y}.pbf".format(y=y)
            filesystem.writebytes(output_path, tiledata)
