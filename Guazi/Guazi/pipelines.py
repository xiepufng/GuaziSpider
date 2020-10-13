# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql


class GuaziPipeline:
    def process_item(self, item, spider):
        print(item)
        return item


class GuaziMysqlPipeline(object):
    # 链接mysql数据库
    def open_spider(self, spider):
        self.db = pymysql.connect(
            'localhost', 'root', '8888', 'guazidb', charset='utf8'
        )
        self.cursor = self.db.cursor()

    # 插入数据
    def process_item(self, item, spider):
        ins = 'insert into guazitab values(%s,%s,%s,%s,%s)'
        L = [
            item['bran'],
            item['mileage'],
            item['discharge'],
            item['ascription'],
            item['transfer']
        ]
        self.cursor.execute(ins, L)
        self.db.commit()
        return item

    # 断开数据库连接
    def close_spider(self, spider):
        self.cursor.close()
        self.db.close()
