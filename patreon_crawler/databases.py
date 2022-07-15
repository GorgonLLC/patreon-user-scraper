import apsw
from scrapy.utils.project import get_project_settings

class PatreonCrawlerDatabase:
    dbfile  = get_project_settings().get('SQLITE_FILE')
    dbtable = get_project_settings().get('SQLITE_TABLE')

    def __init__(self):
        self.setupDBCon()
        self.createDbTable()
        self.createDbIndexes()

    def setupDBCon(self):
        self.con = apsw.Connection(self.dbfile)
        self.cur = self.con.cursor()

    """
    def dropDbTable(self):
        print("Dropping old table: %s" % self.dbtable )
        self.cur.execute("DROP TABLE IF EXISTS %s" % self.dbtable )
    """

    def closeDB(self):
        self.con.close()

    def __del__(self):
        self.closeDB()

    def createDbTable(self):
        print("Creating table: %s" % self.dbtable)
        cols = "creator_id INTEGER NOT NULL UNIQUE, http_response_code INTEGER NOT NULL, updated_at TEXT NOT NULL, vanity TEXT, name TEXT, data JSON"

        # NOTE:  Use "INSERT OR IGNORE", if you also use: "AdId TEXT NOT NULL UNIQUE"
        sql = "CREATE TABLE IF NOT EXISTS %s (id INTEGER PRIMARY KEY NOT NULL, %s)" % (self.dbtable, cols )

        self.cur.execute(sql)

    def createDbIndexes(self):
        sql = """
                CREATE UNIQUE INDEX IF NOT EXISTS idx_creators_on_creator_id
                ON creators(creator_id);
                CREATE        INDEX IF NOT EXISTS idx_creators_on_vanity
                ON creators(vanity)
                WHERE vanity IS NOT NULL;
                CREATE        INDEX IF NOT EXISTS idx_creators_on_code
                ON creators(http_response_code);
                """
        self.cur.execute(sql)

    def dbExecute(self, *args, **kwargs):
        return self.cur.execute(*args, **kwargs)
