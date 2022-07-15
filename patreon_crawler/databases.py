import apsw
from scrapy.utils.project import get_project_settings

class PatreonCrawlerDatabase:
    dbfile  = get_project_settings().get('SQLITE_FILE')

    def __init__(self):
        self.setupDBCon()
        self.createDDL()

    def setupDBCon(self):
        self.con = apsw.Connection(self.dbfile)
        self.cur = self.con.cursor()

    def closeDB(self):
        self.con.close()

    def __del__(self):
        self.closeDB()

    def createDDL(self):
        print("Creating table: creators")
        sql = """
            CREATE TABLE IF NOT EXISTS creators
            (id INTEGER PRIMARY KEY NOT NULL, creator_id INTEGER NOT NULL UNIQUE, http_response_code INTEGER NOT NULL, updated_at TEXT NOT NULL, data JSON)
        """
        self.cur.execute(sql)

        sql = """
                CREATE UNIQUE INDEX IF NOT EXISTS idx_creators_on_creator_id
                ON creators(creator_id);
                CREATE        INDEX IF NOT EXISTS idx_creators_on_vanity
                ON creators(COALESCE(data ->> '$.pageUser.data.attributes.vanity', data ->> '$.campaign.data.attributes.vanity'));
                CREATE        INDEX IF NOT EXISTS idx_creators_on_code
                ON creators(http_response_code);
                """
        self.cur.execute(sql)

    def dbExecute(self, *args, **kwargs):
        return self.cur.execute(*args, **kwargs)
