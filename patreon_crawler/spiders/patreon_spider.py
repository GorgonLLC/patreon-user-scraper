from datetime import datetime
import itertools
import json
import pytz
import re
import scrapy
from patreon_crawler.databases import PatreonCrawlerDatabase

class PatreonSpider(scrapy.Spider):
    name = "patreon"

    def __init__(self, start_id=1, end_id=None, exclude_saved='t', exclude_ranges='[]', **kwargs):
        self.start_id = int(start_id)
        self.end_id = int(end_id) if end_id else None
        self.exclude_saved = exclude_saved.lower() in ['true', 't', 'yes', 'y']
        self.exclude_ranges = json.loads(exclude_ranges)
        self.database = PatreonCrawlerDatabase()
        super().__init__(**kwargs)

    def start_requests(self):
        iterator = None
        if self.end_id:
            iterator = range(self.start_id, self.end_id)
        else:
            iterator = itertools.count(self.start_id)
        for i in iterator:
            # skip over IDs within provided exclude ranges
            skip = False
            for start, end in self.exclude_ranges:
                if start <= i <= end:
                    skip = True
                    break
            if skip:
                continue
            # skip over IDs that already exist in the database
            if self.exclude_saved:
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
