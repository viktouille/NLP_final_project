# -*- coding: utf-8 -*-
"""
Created on Thu May 28 10:57:47 2020

@author: vik
"""

import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'https://www.nytimes.com/',
            'https://www.wsj.com/',
            'https://www.usatoday.com/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)