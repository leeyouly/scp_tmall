# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScpTmall_AppliancesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    airConditionName = scrapy.Field()
    brand = scrapy.Field()
    sort = scrapy.Field()
    energyGrade = scrapy.Field()
    workingWay = scrapy.Field()
    price = scrapy.Field()
    amount = scrapy.Field()
    store = scrapy.Field()
    update_dt = scrapy.Field()


class TaobaoGoodsItem(scrapy.Item):
    GOODS_NAME = scrapy.Field()         # 商品名称
    GOODS_PRICE = scrapy.Field()        # 价格
    MONTHLY_SALES = scrapy.Field()      # 月销量
    GOODS_URL = scrapy.Field()          # 商品url