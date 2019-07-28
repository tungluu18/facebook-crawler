import re
import json
import scrapy
import pandas as pd

from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser # DEBUGER

from fb_fanpage import debug

REGEX_UID = r';rid=\d+|;id=\d+|\?id=\d+'
REGEX_LOGIN_RDR = r'login\.php\?next'

LOOKUP_ID_URI = "https://lookup-id.com"
FINDMYFID_URI = "https://findmyfbid.com"

class ProfileSpider(scrapy.Spider):
    name = "profile"

    custom_settings = {
        'FEED_EXPORT_FIELDS': ['profile_url', 'uid'],
        'HTTPERROR_ALLOWED_CODES': [404]
    }

    def __init__(self, *args, **kwargs):
        filename = kwargs['from_file']
        df = pd.read_csv(filename)
        self.fb_urls = df['profile_url'].to_list()
        self.start_urls = [FINDMYFID_URI]

    def parse(self, response):
        for url in self.fb_urls:
            uid_obj = self._extract_uid(text=url, fb_url=url)
            if uid_obj is not None:
                yield uid_obj
            else:
                yield FormRequest.from_response(
                    response,
                    formdata={'url': url},
                    callback=self.parse_findmyfid,
                    cb_kwargs=dict(fb_url=url))
        self.logger.info('Scraped {} from findmyfid.com'.format(fb_url))

    def parse_findmyfid(self, response, fb_url):
        res_body = json.loads(response.body_as_unicode())
        return dict(
            profile_url=fb_url,
            uid=res_body['id'])

    # def parse_profile(self, response):
    #     self.logger.info('Scraping profile: {} {}'.format(
    #         response.request.url,
    #         len(self.crawler.engine.slot.inprogress)
    #     ))
    #     if True or re.search(REGEX_LOGIN_RDR, response.request.url) is not None:
    #         self.logger.info(response.meta.get('profile_url'))
    #         yield scrapy.Request(
    #             # url=LOOKUP_PAGE_URL,
    #             callback=self.parse_lookup,
    #             meta=response.meta)
    #     else:
    #         uid_obj = self._extract_uid(response.text, response)
    #         if uid_obj: yield uid_obj

    # def parse_lookup(self, response, fb_link):
    #     open_in_browser(response)
    #     return FormRequest.from_response(
    #         response,
    #         formdata={'check': 'Lookup', 'fburl': fb_link},
    #         callback=self.parse_lookup_result,
    #         meta=response.meta)

    # def parse_lookup_result(self, response):
    #     uid = response.css('span[id="code"]::text').get()
    #     self.logger.info('Scraped from look-up.com: {} {}'.format(response.meta.get('profile_url'), uid))
    #     return {
    #         'uid': uid,
    #         'profile_url': response.meta.get('profile_url')
    #     }

    @staticmethod
    def _extract_uid(text: str, fb_url=None):
        uid_matches = re.findall(REGEX_UID, text)
        if len(uid_matches):
            uid = ''.join([n for n in uid_matches[0] if n.isdigit()])
            return dict(
                uid=uid,
                profile_url=fb_url)
        return None
