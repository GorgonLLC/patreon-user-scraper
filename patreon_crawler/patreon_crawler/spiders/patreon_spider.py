import scrapy
import re
import json

class PatreonSpider(scrapy.Spider):
    name = "patreon"

    def start_requests(self):
        for i in range(1, 2):
            url = 'https://www.patreon.com/user?u={}'.format(i)
            request = scrapy.Request(
                url=url,
                callback=self.parse,
                cb_kwargs=dict(user_id=i))
            yield request

    def parse(self, response, user_id):
        result = {
            'id': user_id,
        }

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
        print(result)
