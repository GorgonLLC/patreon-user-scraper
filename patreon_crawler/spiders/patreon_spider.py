from datetime import datetime
import json
import pytz
import re
import scrapy
from patreon_crawler.databases import PatreonCrawlerDatabase

class PatreonSpider(scrapy.Spider):
    name = "patreon"

    def __init__(self, start_id=1, end_id=100000, skip_saved='t', skip_ranges='[]', **kwargs):
        self.start_id = int(start_id)
        self.end_id = int(end_id)
        self.skip_saved = skip_saved.lower() in ['true', 't', 'yes', 'y']
        self.skip_ranges = json.loads(skip_ranges)
        self.database = PatreonCrawlerDatabase()
        super().__init__(**kwargs)

    def start_requests(self):
        for i in range(self.start_id, self.end_id):
            # skip over IDs within provided skip ranges
            skip = False
            for start, end in self.skip_ranges:
                if start <= i <= end:
                    skip = True
                    break
            if skip:
                continue
            # skip over IDs that already exist in the database
            if self.skip_saved:
                for row in self.database.dbExecute("SELECT 1 FROM creators WHERE creator_id = ?", (i,)):
                    skip = True
                if skip:
                    continue
            url = 'https://www.patreon.com/user?u={}'.format(i)
            request = scrapy.Request(
                url=url,
                callback=self.parse,
                # handle 404s (we don't want handle_httpstatus_all because then
                # we'd disable automatic redirect handling)
                meta=dict(handle_httpstatus_list=[404]),
                cb_kwargs=dict(creator_id=i))
            yield request

    def parse(self, response, creator_id):
        result = {
            'creator_id': creator_id,
            'http_response_code': response.status,
            'updated_at': datetime.now(tz=pytz.UTC).isoformat(),
        }
        # We won't have creator data for 404s
        if response.status != 200:
            return result

        xs = response.xpath("//script[contains(text(),'window.patreon.bootstrap')]")
        for x in xs:
            # get the full user data as JSON
            full_data_pattern = 'Object\.assign\(window\.patreon\.bootstrap, \{(.*?)^\}\);'
            m = re.search(full_data_pattern, x.get(), re.DOTALL | re.MULTILINE)
            if m:
                result['data'] = json.loads('{%s}' % m.group(1))
        return result
