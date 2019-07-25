import scrapy
import logging
import re

import pandas as pd
from scrapy.http import FormRequest

class FanpageSpider(scrapy.Spider):
    name = "fanpage"

    custom_settings = {
        'FEED_EXPORT_FIELDS': ['profile_url']
    }

    email = "tungcl0n3.1@gmail.com"
    password = "tungclone1"

    # group_id = 'Divine.Shop.Steam'
    # post_id = '2302909819763234'
    # posts_id = []
    link = None

    def __init__(self, *args, **kwargs):
        logger = logging.getLogger('scrappy.middleware')
        logger.setLevel(logging.WARNING)
        super().__init__(*args, **kwargs)
        if 'page' in kwargs:
            self.link = '/{page}/posts/'.format(**kwargs),
            self.link = self.link[0]
        else:
            self._link = '/groups/{group}/posts/'.format(**kwargs),
            self.link = self.link[0]
        # get post ids from csv file
        filename = kwargs['from_file']
        df = pd.read_csv(filename)
        self.posts_id = df['post_id'].to_list()
        # self.posts_id = ['1000971710027220']
        self.start_urls = [
            'https://mbasic.facebook.com'
        ]

    def parse(self, response):
        # login
        return FormRequest.from_response(
            response,
            formxpath='//form[contains(@action, "login")]',
            formdata={'email' : self.email, 'pass': self.password},
            callback=self.parse_home)

    def parse_home(self, response):
         #handle 'save-device' redirection
        if response.xpath("//div/a[contains(@href,'save-device')]"):
            self.logger.info('Going through the "save-device" checkpoint')
            yield FormRequest.from_response(
                response,
                formdata={'name_action_selected': 'dont_save'},
                callback=self.parse_home)
        # navigate to posts
        for post_id in self.posts_id:
            href = response.urljoin('{}{}'.format(self.link, post_id))
            self.logger.info('Scrapping facebook page {}'.format(href))
            yield scrapy.Request(url=href, callback=self.parse_post)

    def parse_post(self, response):
        reaction_div = response.css('[id^="sentence"]')
        reaction_href = reaction_div.css('a::attr(href)').get()
        return response.follow(reaction_href, self.parse_reactions)

    def parse_reactions(self, response):
        # with open("crossfire.html", "wb") as f:
        #     f.write(response.body)
        # return
        self.logger.info(response.request.url)
        reaction_list = response.css('ul')
        lines = reaction_list.css('li')
        hrefs = []
        next_page = None
        for line in lines:
            href = line.css('a::attr(href)').extract_first()
            if href[:5] == '/ufi/':
                next_page = href
            else:
                yield {'profile_url': 'https://facebook.com{}'.format(href)}

        if next_page is not None:
            # self.page_counter += 1
            # self.logger.info('next_page {}'.format(self.page_counter))
            yield response.follow(
                url=next_page,
                callback=self.parse_reactions)
