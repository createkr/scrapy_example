import scrapy

from douban.items import DoubanItem



class MovieSpider(scrapy.Spider):
    name = "movie"
    allowed_domains = ["douban.com"]
    start_urls = ["https://movie.douban.com/top250"]


    def parse(self, response):
        # print(response.headers['User-Agent'])
        el_list = response.xpath('//*[@class="info"]')
        print(len(el_list))
        for el in el_list:
            item = DoubanItem()
            item["name"] =  el.xpath('./div[1]/a/span[1]/text()').extract_first()
            item["info"] = el.xpath('./div[2]/p/text()').extract_first()
            item["score"] = el.xpath('./div[2]/div/span[2]/text()').extract_first()
            item["desc"] = el.xpath('./div[2]/p[2]/span/text()').extract_first()
            # print(item)
            yield  item

        #
        next_url = response.xpath('//span[@class="next"]/a/@href').extract_first()
        if next_url is not None:
            url = response.urljoin(next_url)
            yield scrapy.Request(
                url,
                callback=self.parse
            )