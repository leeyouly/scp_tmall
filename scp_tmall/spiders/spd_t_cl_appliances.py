# -*- coding: UTF-8 -*-
import scrapy
from scrapy.utils.project import get_project_settings
from scp_tmall.items import  ScpTmall_AppliancesItem
import re
import os
import time, datetime
import sys
reload(sys)
sys.setdefaultencoding('utf8')

today = datetime.datetime.now()
day_datadate = today.strftime('%Y-%m-%d')
year_datadate = today.strftime('%Y')
last_year = int(year_datadate) - 1
last_update_date = datetime.datetime.now() - datetime.timedelta(days=10)

#天猫家电销量数据抓取
class CL_Tombarthite(scrapy.Spider):
    name = "spd_t_cl_appliances"
    start_urls = (
        'https://www.tmall.com/',
    )
    ignore_page_incremental = True

    def parse(self,response):
        self.crawler.stats.set_value('spiderlog/source_name', u'天猫')
        self.crawler.stats.set_value('spiderlog/target_tables', ['t_cl_appliances'])
        # urlstart = response.xpath('//*[@id="sogou_vr_11002301_box_0"]/div/div[2]/p[1]/a/@href').extract()[0]
        cookie = {
            '_med':'dw:1536&dh:864&pw:1920&ph:1080&ist:0',
            'pnm_cku822':'098%23E1hvPpvUvbpvUvCkvvvvvjiPPFdOAjYVP2cwtj3mPmP9QjnmRssv6j1hP25Z6jE2iQhvCvvv9UUCvpvVvvpvvhCvmphvLC2FD9vj7dmxfaoKHsCHs4V9D40wjLoQD7zpditApRm%2BD70OdeQEfwBlYb8raAuOD7zpd3ODNrBlKWVTKo9vD7zhaXp7EcqhaNoxdXutvpvIvvvvEyCvvvvvvvWvphvU%2BQvvvQCvpvACvvv2vhCv2RvvvvWjphvWVOyCvvOUvvVvaZJivpvUvvmv%2BLjJtO%2BPvpvhvv2MMsyCvvpvvvvv',
            'cq':'ccp%3D1',
            'tt':'tmall-main',
            'res':'scroll%3A1524*5570-client%3A1524*748-offset%3A1524*5570-screen%3A1536*864',
            'tk_trace':'1',
            't':'9cef72811c2a7577c968b2afd9d87492',
            '_tb_token_':'3ee56510eb1e6',
            'cookie2':'1e4d4186ef2b99065952a20745cc1a45',
            'enc':'EeuMq3gMmG5fD6SEj1LyUa9VtSCQkJLm91USt2g2vNatOHMZDLxyFZwPZItAbJ2YbgXEDBgoenpmSvD%2BATtFKA%3D%3D',
            'cna':'Eh7+EXkBEB4CAXFi79pGkVmX',
            'isg':'BLKy782hPDNqGwAPk8HXY1_wGviUQ7bdx9Ct-nyKCWVQD1AJZdDg7B4p-ymzZC51',
        }
        urlstart = 'https://list.tmall.com/search_product.htm?spm=a220m.1000858.1000724.9.5ac12fdejSgQwj&cat=50930001&q=%BF%D5%B5%F7&sort=s&style=l&search_condition=23&from=sn_1_rightnav&industryCatId=50930001#J_Filter'
        urlstart = 'https://list.tmall.com/search_product.htm?spm=a220m.1000858.1000724.9.7bd61490KwkXoG&q=%BF%D5%B5%F7&sort=s&style=l&from=.list.pc_1_searchbutton&smToken=96eec504efe843ae95f9f2403312a566&smSign=YUGqUZUexcrqHAMU3cY5RQ%3D%3D'
        urlstart = 'https://list.tmall.com/search_product.htm?spm=a220m.1000858.1000724.9.1f781490xRyDHl&q=%BF%D5%B5%F7&sort=s&style=l&from=mallfp..pc_1_searchbutton&smToken=5bd40a50bb8848cfa681d92dddf5b014&smSign=UVBzDk5PcnGfKU6fBgZg9w%3D%3D'
        urlstart = 'https://list.tmall.com/search_product.htm?spm=a220m.1000858.1000724.9.625014900dJD6n&q=%BF%D5%B5%F7&sort=s&style=l&from=mallfp..pc_1_searchbutton&active=2#J_Filter'
        request = scrapy.http.Request(urlstart, callback=self.parse_content,cookies=cookie)
        yield request

    #处理返回的请求
    def parse_content(self, response):
        contentStr = response.body
        goodsList = response.xpath('//*[@id="J_ItemList"]/div')

        for goods in goodsList:
            airConditionerName = response.xpath('./div/div[@class="prodectInfo"]/div[@class="prodectTitle"]/h4/a/text()').extract()[0]
            brand = response.xpath('./div/div[@class="prodect-limited"]/div[@class="productAttrs"]/span[1]/text()').extract()[0]
            sort = response.xpath('./div/div[@class="prodect-limited"]/div[@class="productAttrs"]/span[2]/a/text()').extract()[0]
            energyGrade = response.xpath('./div/div[@class="prodect-limited"]/div[@class="productAttrs"]/span[3]/a/text()').extract()[0]
            workingWay = response.xpath('./div/div[@class="prodect-limited"]/div[@class="productAttrs"]/span[4]/a/text()').extract()[0]
            price = response.xpath('./div/div[@class="prodectInfo"]/p[1]/em/text()').extract()[0]
            amount = response.xpath('./div/div[@class="prodectInfo"]/p[@class="productStatus"]/em/text()').extract()[0]
            store = response.xpath('./div/div[@class="prodectInfo"]/p[@class="productShop"]/a/text()').extract()[0]

        listStr = re.findall('var msgList = (.+);', contentStr)
        if listStr <> []:
            titleList = eval(re.findall('var msgList = (.+);',contentStr)[0])
            for title in titleList['list']:
                releaseTimestamp = title['comm_msg_info']['datetime']
                t = time.localtime(time.time())
                timeZero = time.mktime(time.strptime(time.strftime('%Y-%m-%d 00:00:00', t), '%Y-%m-%d %H:%M:%S'))

                timeStamp = title['comm_msg_info']['datetime']
                timeArray = time.localtime(timeStamp)
                # releaseTime = time.strptime(time.strftime("%Y-%m-%d %H:%M:%S", timeArray), '%Y-%m-%d %H:%M:%S')
                releaseTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)


                if u'稀土早报' in title['app_msg_ext_info']['title']:
                    titleUrl = 'https://mp.weixin.qq.com' + title['app_msg_ext_info']['content_url'].replace('amp;','')
                    author = title['app_msg_ext_info']['author']
                    digest = title['app_msg_ext_info']['digest']
                    title = title['app_msg_ext_info']['title']
                    request = scrapy.http.Request(titleUrl, callback=self.parse_news)
                    request.meta['title'] = title
                    request.meta['datadate'] = releaseTime
                    yield request
        else:
            print u'未找到文章列表'


    def parse_news(self, response):
        datadate = datetime.datetime.strptime(response.meta['datadate'], '%Y-%m-%d %H:%M:%S')
        viewpoint = response.xpath('//*[@id="js_content"]/section[2]/section/section/p/text()').extract()[0]

        contentHtml = response.xpath('//*[@id="js_content"]/blockquote[1]/section/p')
        contentString1 = ''
        for content in contentHtml:
            if content.xpath('.//text()').extract()<>[] :

                for contentStr in content.xpath('.//text()').extract():
                    contentString1 = contentString1 + contentStr
                contentString1 = contentString1 + '\n'

        print response.meta['datadate'] +'------'+ viewpoint
        print contentString1

        item = ScpTmall_AppliancesItem()
        item['datadate'] = datadate
        item['news_title'] = response.meta['title']
        item['viewpoint'] = viewpoint
        item['news_html'] = u''
        item['public_Id'] = 'gh_aff6576c52c9'
        item['public_name'] = u'稀土在线'
        item['update_dt'] = datetime.datetime.now()
        item['news_content'] = contentString1
        yield item