import scrapy
from ..items import GuaziItem


class GuaziSpider(scrapy.Spider):
    name = 'guazi'
    allowed_domains = ['www.guazi.com']
    url = 'https://www.guazi.com/gz/buy/o{}/#bread'
    headers = {

        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": "uuid=61c1007d-c3ef-4df7-8740-d3a10da0f343; clueSourceCode=%2A%2300; ganji_uuid=6329452022214993090088; sessionid=c3db053d-b291-4ecb-cc78-c584c55bcf52; lg=1; _gl_tracker=%7B%22ca_source%22%3A%22-%22%2C%22ca_name%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_id%22%3A%22-%22%2C%22ca_s%22%3A%22self%22%2C%22ca_n%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22sid%22%3A58045776418%7D; cainfo=%7B%22ca_a%22%3A%22-%22%2C%22ca_b%22%3A%22-%22%2C%22ca_s%22%3A%22self%22%2C%22ca_n%22%3A%22self%22%2C%22ca_medium%22%3A%22-%22%2C%22ca_term%22%3A%22-%22%2C%22ca_content%22%3A%22-%22%2C%22ca_campaign%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22scode%22%3A%22-%22%2C%22keyword%22%3A%22-%22%2C%22ca_keywordid%22%3A%22-%22%2C%22display_finance_flag%22%3A%22-%22%2C%22platform%22%3A%221%22%2C%22version%22%3A1%2C%22client_ab%22%3A%22-%22%2C%22guid%22%3A%2261c1007d-c3ef-4df7-8740-d3a10da0f343%22%2C%22ca_city%22%3A%22gz%22%2C%22sessionid%22%3A%22c3db053d-b291-4ecb-cc78-c584c55bcf52%22%7D; user_city_id=16; preTime=%7B%22last%22%3A1602398935%2C%22this%22%3A1602317625%2C%22pre%22%3A1602317625%7D; cityDomain=langfang; rfnl=https://www.guazi.com/gz/buy/; antipas=7374g7522195u6ja12703t954193",
        "Host": "www.guazi.com",
        "Referer": "https://www.guazi.com/gz/buy/",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36"

    }

    def start_requests(self):
        for pn in range(1, 51):
            url = self.url.format(pn)
            yield scrapy.Request(
                url=url,
                headers=self.headers,
                callback=self.parse)

    def parse(self, response):
        link_list = response.xpath('//ul[@class="carlist clearfix js-top"]/li/a/@href').extract()
        for link in link_list:
            url = 'https://www.guazi.com' + link
            yield scrapy.Request(
                url=url,
                headers=self.headers,
                callback=self.two_parse)

    def two_parse(self, response):
        item = GuaziItem()
        item['bran'] = response.xpath('//h2[@id="base"]/span/text()').get().strip()[:-5]
        item['mileage'] = response.xpath('//li[@class="two"]/div/text()').get().strip()
        item['discharge'] = response.xpath('//li[@class="four"]/div[@class="typebox"]/text()').get().strip()
        item['ascription'] = response.xpath('//li[@class="ten"]/div[@class="typebox"]/text()').get().strip()
        item['transfer'] = response.xpath('//li[@class="seven"]/div[@class="typebox"]/text()').get().strip()
        yield item
