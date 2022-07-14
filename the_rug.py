#!/usr/bin/env python
# coding: utf-8

# In[1]:


import scrapy

class rug_shop(scrapy.Spider):
    name = 'rug'
    allowed_domains = ['www.therugshopuk.co.uk']
    start_urls = ['https://www.therugshopuk.co.uk/rugs-by-type/rugs.html?p=1']
    custom_settings = {"FEEDS":{"rug.csv":{"format":"csv"}}}
    
    def parse(self,response):
        for i in range(1,158):
            products = response.xpath("//li[@class='item product product-item']")
            for product in products:
                link = product.css('a.product-item-link').attrib['href']
                yield scrapy.Request(url = link, callback= self.parse_details)
         #pagination   
            next_p = f'https://www.therugshopuk.co.uk/rugs-by-type/rugs.html?p={i}'
            yield scrapy.Request(url = next_p,callback=self.parse)
            
    def parse_details(self,response):
        name = response.css('span.base::text').extract_first()
        product_id = response.css('div.pdp_product_id::text').extract_first().replace('Product Id : ', '')
        material = response.css('span.prod_mat::text').extract_first().strip()
        price = response.css('span.price::text').extract_first()
        yield {
            'Name':name,
            'Product Id':product_id,
            'Price':price,
            'Material':material,
        }

