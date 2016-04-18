# -*- coding: utf-8 -*-
import cgi
import re
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import FormRequest

from halal.items import HalalItem


class HalalCrawlerSpider(CrawlSpider):
    name = 'halal_crawler'
    allowed_domains = ['www.halal.gov.my']
    page = 1
    total_page = 0
    url = 'http://www.halal.gov.my/ehalal/directory_standalone.php'

    def __init__(self, keyword=''):
        self.keyword = keyword

    def start_requests(self):
        return [FormRequest(self.url,
                            formdata={'cari': self.keyword},
                            callback=self.parse_item)]


    @staticmethod
    def regex_item(pattern, val, group, clean=True):
        val = re.search(pattern, val, re.I)
        if val:
            val = val.group(group)
            val = HalalCrawlerSpider.clean(val)
            #clean
            if clean:
                val = val.strip()
        else:
            val = ''
        return val

    @staticmethod
    def strip_tags(val):
        # regex to remove html tags
        tag_re = re.compile(r'(<!--.*?-->|<[^>]*>)')
        val = tag_re.sub('', val)
        val = cgi.escape(val)
        val = HalalCrawlerSpider.clean(val)
        return val

    @staticmethod
    def clean(val):
        val = val.replace("&nbsp", "")
        val = val.strip()
        return val

    def parse_item(self, response):
        rows = response.xpath('//table[@id="gradient-style"]/tr[position()>1]')
        #from scrapy.shell import inspect_response
        #inspect_response(response, self)
        for row in rows:
            i = HalalItem()
            product = row.xpath('td[2]').extract()[0]
            product = product.split("<br>")

            if len(product) == 3:
                #full listing (name,brand,company
                name = self.strip_tags(product[0]).strip()
                brand = self.strip_tags(product[1]).strip()[7:]
                company_name = self.strip_tags(product[2]).strip()[1:]
            else:
                #no brand
                name = self.strip_tags(product[0]).strip()
                company_name = self.strip_tags(product[1]).strip()[1:]
                brand = ''

            i['name'] = name
            i['brand'] = brand
            i['companyName'] = company_name
            #company code is in column 4
            company_code = row.xpath('td[4]/img/@onclick').extract()[0]
            i['companyCode'] = self.regex_item(r'comp_code=(.+?)&', company_code, 1)
            #expiry  is in column 4
            i['expiry'] = self.strip_tags(row.xpath('td[3]').extract()[0]).strip()
            yield i

            if self.page == 1:
                # pagination code starts here
                # first time
                pages = response.xpath('//table/tr/td[@class="corporatedesc"]/div/b[contains(.,"Record")]/text()')\
                    .extract()
                if pages:
                    pages = pages[0]
                    total = re.search(r'From.+?([\d]+)', pages, re.I)
                    self.total_page = int(total.group(1))

            if self.total_page >= self.page:
                # crawl pagination
                self.page += 1
                formdata = {
                    'cari': self.keyword
                }
                yield FormRequest(url=self.url + "?page=" + str(self.page), formdata=formdata, callback=self.parse_item)



