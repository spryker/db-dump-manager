import psycopg2


class TableReader:
    __all_table_query__ = "SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND " \
                          "table_type='BASE TABLE'; "

    def __init__(self, dbname, user, password, host='localhost', port=5432):
        self.port = port
        self.host = host
        self.password = password
        self.user = user
        self.dbname = dbname

    # todo: dict
    def get_connection(self):
        return psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )

    def get_table_name_list(self):
        pg_connection = self.get_connection()

        pg_cursor = pg_connection.cursor()
        pg_cursor.execute('SELECT table_name\n' +
                          '  FROM information_schema.tables\n' +
                          ' WHERE table_schema=\'public\'\n' +
                          '   AND table_type=\'BASE TABLE\';')
        records = pg_cursor.fetchall()

        pg_cursor.close()
        pg_connection.close()

        return [i for record in records for i in record]
