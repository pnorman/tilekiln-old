import jinja2 as j2


class Definition:
    ''' Definition of a layer in a particular zoom range.

    This class does the work of producing the SQL query for a particular tile.
    '''
    def __init__(self, id, raw_sql, minzoom, maxzoom):
        self.id = id
        self.raw_sql = raw_sql
        self.minzoom = minzoom
        self.maxzoom = maxzoom

    def __eq__(self, other):
        return (self.id == other.id and self.raw_sql == other.raw_sql and
                self.minzoom == other.minzoom and
                self.maxzoom == other.maxzoom)

    def __repr__(self):
        return 'Definition({}, "{}", {}, {}'.format(self.id, self.raw_sql,
                                                    self.minzoom, self.maxzoom)

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
        j2_template = j2.Template(wrap_sql(self.raw_sql, self.id))
        return j2_template.render(zoom=zoom, x=x, y=y,
                                  bbox=bbox(zoom, x, y))


# Utility functions
def wrap_sql(sql, layer_id):
    return ('''WITH mvtgeom AS\n(\n''' + sql + '''\n)\n''' +
            '''SELECT ST_AsMVT(mvtgeom.*, '{}', '''.format(layer_id) +
            '''4096, 'way', NULL)\n'''
            '''FROM mvtgeom;''')


def bbox(zoom, x, y):
    ''' Returns an array of [minx, miny, max, maxy]
        There is a flip of y axis converting between xyz and EPSG:3857
    '''
    ll = zxy_to_projected(zoom, x, y)
    ur = zxy_to_projected(zoom, x+1, y+1)
    return ('ST_MakeEnvelope({}, {}, {}, {}, 3857)'
            .format(ll[0], ur[1], ur[0], ll[1]))


# ref https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames
#     https://github.com/mapbox/postgis-vt-util/blob/master/src/TileBBox.sql
#     and others.
def zxy_to_projected(zoom, x, y):
    HALF_WORLD = 20037508.34
    return [HALF_WORLD*(2*x/2**zoom - 1),
            HALF_WORLD*(1-2*y/2**zoom)]
