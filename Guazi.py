import requests
import time
import random
from lxml import etree


class GuaziSpider(object):
    def __init__(self):
        self.session = requests.session()
        #　瓜子网采用cookie 反爬，定义请求头
        self.headers = {

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
        self.url = 'https://www.guazi.com/gz/buy/o{}/#bread'
        # 爬取车辆数
        self.num=0

    # 定义爬取页面函数，减少requests模块的复用
    def get_page(self, url):
        html = self.session.get(url=url, headers=self.headers).text
        return html

    # 定义解析函数，减少etree模块的复用
    def parse_html(self, html, xpath_bds):
        parse_html = etree.HTML(html)
        targer_list = parse_html.xpath(xpath_bds)
        return targer_list

    # 定义一级页面函数，获取耳机页面的链接
    def get_one_page(self):
        for pn in range(1, 51):
            url = self.url.format(pn)
            html = self.get_page(url=url)
            time.sleep(2)
            # print(html)
            print('*' * 20)
            link_list = self.parse_html(html=html, xpath_bds='//ul[@class="carlist clearfix js-top"]/li/a/@href')
            # print(link_list)
            for link in link_list:
                url = 'https://www.guazi.com' + link
                # print(url)
                self.get_two_page(url)
                # 每爬取一页，随机休眠１到２秒，防止ｉｐ被封
                time.sleep(random.randint(1,2))

    # 获取二级页面并解析所需车辆信息
    def get_two_page(self, link):
        html = self.session.get(url=link, headers=self.headers).text
        # 车辆基本信息
        bran = self.parse_html(html=html, xpath_bds='//h2[@id="base"]/span/text()')[0].strip()
        # 行驶公里数
        mileage = self.parse_html(html, xpath_bds='//li[@class="two"]/div/text()')[0].strip()
        # 环保等级
        discharge = self.parse_html(html, xpath_bds='//li[@class="four"]/div[@class="typebox"]/text()')[0].strip()
        # 产权
        ascription = self.parse_html(html, xpath_bds='//li[@class="ten"]/div[@class="typebox"]/text()')[0].strip()
        # 过户次数
        transfer = self.parse_html(html, xpath_bds='//li[@class="seven"]/div[@class="typebox"]/text()')[0].strip()

        print(bran,mileage,discharge,ascription,transfer)
        self.num+=1
    # 主函数
    def main(self):
        self.get_one_page()
        print('抓取%s辆车'%self.num)


if __name__ == '__main__':
    start=time.time()
    Guazi = GuaziSpider()
    Guazi.main()
    end=time.time()
    print('爬取时间为%2.f'%(end-start))