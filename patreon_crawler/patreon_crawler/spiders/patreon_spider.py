import datetime
import json
import re
import scrapy

class PatreonSpider(scrapy.Spider):
    name = "patreon"

    def __init__(self, start_id=1, end_id=100000, **kwargs):
        self.start_id = int(start_id)
        self.end_id = int(end_id)
        super().__init__(**kwargs)

    def start_requests(self):
        for i in range(self.start_id, self.end_id):
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
            'updated_at': datetime.datetime.now().astimezone().isoformat(),
        }
        # We won't have creator data for 404s
        if response.status != 200:
            return result

        xs = response.xpath("//script[contains(text(),'window.patreon.bootstrap')]")
        for x in xs:
            s = x.get()
            # get some of the basic data
            basic_patterns = {
                'vanity': '^\s*"vanity":\s*"([^"]+)"',
                'name': '^\s*"name":\s*"([^"]+)"',
                #'summary': '^\s*"summary":\s*"([^"]+)"',
            }
            for name, pattern in basic_patterns.items():
                m = re.search(pattern, s, re.DOTALL | re.MULTILINE)
                if m:
                    result[name] = m.group(1)
            # get the full user data as JSON
            full_data_pattern = 'Object\.assign\(window\.patreon\.bootstrap, \{(.*?)^\}\);'
            m = re.search(full_data_pattern, s, re.DOTALL | re.MULTILINE)
            if m:
                result['data'] = json.loads('{%s}' % m.group(1))
        return result
