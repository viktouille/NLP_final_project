import scrapy
from NLP_spider.items import NYTItem
from NLP_spider.pipelines import NYTPipeline

class NYTSpider(scrapy.Spider):
    name = "NYT"
    allowed_domains = ["nytimes.com"]
    start_urls = ["https://spiderbites.nytimes.com/2020/"]
    baseURL1 = "http://spiderbites.nytimes.com"
    baseURL2 = "http://www.nytimes.com/"
    pipeline = set([NYTPipeline])

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for url in response.xpath('//div[@class="articlesMonth"]/ul/li/a/@href').extract():
            yield scrapy.Request(self.baseURL1 + url, callback = self.parseNews)        


    def parseNews(self, response):
        News = []
        News_urls = response.xpath('//ul[@id="headlines"]/li/a/@href').extract()
        News.extend([self.make_requests_from_url(url).replace(callback=self.parseSave) for url in News_urls])

        return News

    def parseSave(self, response):
        item = NYTItem()

        item["link"] = response.url
        try:
            item["category"] = response.xpath('//meta[@name="byl"]/@content').extract()[0]
        except IndexError:
            item["category"] = ""
        item["title"] = response.xpath('//meta[@property="og:title"]/@content').extract()[0]
        try:
            item["author"] = response.xpath('//meta[@name="byl"]/@content').extract()[0]
        except IndexError:
            item["auhor"] = ""
        try:
            item["date"] = response.xpath('//meta[@property="article:published"]/@content').extract()[0]
        except IndexError:
            item["date"] = ""
        item["article"] = response.xpath('//p/descendant-or-self::*/text()').extract()

        yield item
