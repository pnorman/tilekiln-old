import jinja2 as j2


# Invariants of web mercator
HALF_WORLD = 20037508.34


class Definition:
    ''' Definition of a layer in a particular zoom range.

    This class does the work of producing the SQL query for a particular tile.
    '''
    def __init__(self, id, raw_sql, minzoom, maxzoom, extent, buffer):
        self.id = id
        self.raw_sql = raw_sql
        self.minzoom = minzoom
        self.maxzoom = maxzoom

        self.extent = extent or 4096
        self.buffer = buffer or 0

    def __eq__(self, other):
        return (self.id == other.id and self.raw_sql == other.raw_sql and
                self.minzoom == other.minzoom and
                self.maxzoom == other.maxzoom and
                self.extent == other.extent and
                self.buffer == other.buffer)

    def __repr__(self):
        return ('Definition({}, "{}", {}, {}, {})'
                .format(self.id, self.raw_sql, self.minzoom, self.maxzoom,
                        self.extent))

    def render_sql(self, tile):
        '''Generates the SQL for a layer
        '''
        zoom, x, y = tile
        assert(zoom >= self.minzoom)
        assert(zoom <= self.maxzoom)
        assert(x >= 0)
        assert(x < 2**zoom)
        assert(y >= 0)
        assert(y < 2**zoom)

        # See See https://postgis.net/docs/ST_AsMVT.html for SQL source
        # TODO: Add parameters for all ST_AsMVT and ST_AsMVTGeom options
        sql = j2.Template(self.raw_sql)

        inner = sql.render(zoom=zoom, x=x, y=y,
                           tile_length=tile_length(zoom),
                           tile_area=tile_area(zoom),
                           coordinate_length=coordinate_length(zoom,
                                                               self.extent),
                           coordinate_area=coordinate_area(zoom,
                                                           self.extent),
                           extent=self.extent, buffer=self.buffer,
                           bbox=bbox(zoom, x, y, self.buffer/self.extent),
                           unbuffered_bbox=bbox(zoom, x, y, 0))

        return wrap_sql(inner, self.id, self.extent)


# Utility functions
def wrap_sql(sql, layer_id, extent):
    return ('''WITH mvtgeom AS\n(\n''' + sql + '''\n)\n''' +
            '''SELECT ST_AsMVT(mvtgeom.*, '{}', '''.format(layer_id) +
            '''{}, 'way', NULL)\n'''.format(extent) +
            '''FROM mvtgeom;''')


def bbox(zoom, x, y, buffer):
    ''' Returns an array of [minx, miny, max, maxy]
        There is a flip of y axis converting between xyz and EPSG:3857
    '''
    ll = zxy_to_projected(zoom, x-buffer, y-buffer)
    ur = zxy_to_projected(zoom, x+1+buffer, y+1+buffer)
    return ('ST_MakeEnvelope({}, {}, {}, {}, 3857)'
            .format(ll[0], ur[1], ur[0], ll[1]))


def tile_length(zoom):
    # -1 for half vs full world
    return HALF_WORLD/(2**(zoom-1))


def coordinate_length(zoom, extent):
    return tile_length(zoom)/extent


def tile_area(zoom):
    return tile_length(zoom)**2


def coordinate_area(zoom, extent):
    return coordinate_length(zoom, extent)**2


# ref https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames
#     https://github.com/mapbox/postgis-vt-util/blob/master/src/TileBBox.sql
#     and others.
def zxy_to_projected(zoom, x, y):
    return [HALF_WORLD*(2*x/2**zoom - 1),
            HALF_WORLD*(1-2*y/2**zoom)]
