import re
import scrapy
import pandas as pd

from scrapy.http import FormRequest

REGEX_UID = r';rid=\d+|;id=\d+|\?id=\d+'

class ProfileSpider(scrapy.Spider):
    name = "profile"

    custom_settings = {
        'FEED_EXPORT_FIELDS': ['profile_url', 'uid'],
        'DOWNLOAD_DELAY': 0.2
    }

    def __init__(self, *args, **kwargs):
        filename = kwargs['from_file']
        df = pd.read_csv(filename)
        self.urls = df['profile_url'].to_list()
        self.hrefs = [url.replace('https://facebook.com', '') for url in self.urls]
        self.start_urls = ['https://mbasic.facebook.com']

    def parse(self, response):
        for href in self.hrefs:
            uid_obj = self._extract_uid(href, response)
            if uid_obj:
                yield uid_obj
            else:
                yield response.follow(href, callback=self.parse_profile)

    def parse_profile(self, response):
        self.logger.info('Scraping profile: {}'.format(response.request.url))
        uid_obj = self._extract_uid(response.text, response)
        if uid_obj: yield uid_obj

    @staticmethod
    def _extract_uid(text: str, response=None):
        uid_matches = re.findall(REGEX_UID, text)
        if len(uid_matches):
            uid = ''.join([n for n in uid_matches[0] if n.isdigit()])
            return {
                'uid': uid,
                'profile_url': response.request.url.replace('mbasic.', '') if response else None
            }
        return None
