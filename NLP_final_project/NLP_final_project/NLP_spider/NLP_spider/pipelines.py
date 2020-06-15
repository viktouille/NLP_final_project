# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from pathlib import Path
import logging
from scrapy import logformatter

class NlpSpiderPipeline:
    def process_item(self, item, spider):
        return item


class NYTPipeline(object):
	def __init__(self):
		self.titles_seen = set()
		self.directory = "NYT_scraped/"
		Path(self.directory).mkdir(parents=True, exist_ok=True)

	def process_item(self, item, spider):
		filename = item["title"].translate({ord(c): "_" for c in " !@#$%^&*()[]{};:,./<>?\|`~-=_+"}) + ".txt"
		logging.info("*** Saving article in: " + filename)
		if filename in self.titles_seen:
			return None
		else:
			self.titles_seen.add(filename)
			with open(self.directory + '%s' % filename, 'w+b') as f:
				content = item["link"] + '\n' + '\n' + item["category"] + '\n' + '\n' + item["title"] +'\n' + '\n' + item["author"] +'\n' + '\n' + item["date"] +'\n' + '\n' 
				f.write(content.encode())
				for p in item["article"]:
					if p != None :
						f.write(p.encode() + '\n'.encode())
