class Database:
    '''A wrapper for a psycopg2 connection

    A Database produces a tile-layer, given a definition
    '''
    def __init__(self, conn):
        self.conn = conn

    def generate_tilelayer(self, definition, tile):
        with self.conn.cursor() as curs:
            sql = definition.render_sql(tile)
            curs.execute(sql)
            result = curs.fetchone()
            mvt = result[0]

        return mvt
