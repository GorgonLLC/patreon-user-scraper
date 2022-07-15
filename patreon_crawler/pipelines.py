# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
from patreon_crawler.databases import PatreonCrawlerDatabase

class PatreonCrawlerPipeline:
    def __init__(self):
        self.database = PatreonCrawlerDatabase()

    def storeInDb(self, item):
        # NOTE:  Use "INSERT OR IGNORE", if you also use: "AdId TEXT NOT NULL UNIQUE"
        #update_part = ', '.join(['%s = ?' % k for k in item.keys()])
        #ON CONFLICT(creator_id) DO UPDATE SET {3}
        sql = "INSERT OR REPLACE INTO {0} ({1}) VALUES ({2});".format(self.database.dbtable, ','.join(item.keys()), ','.join(['?'] * len(item.keys())))

        values = []
        for x in item.values():
            # need to convert dicts to JSON string
            if type(x) is dict:
                values.append(json.dumps(x))
            else:
                values.append(x)
        self.database.dbExecute(sql, tuple(values))

    def process_item(self, item, spider):
        self.storeInDb(item)
        return item
