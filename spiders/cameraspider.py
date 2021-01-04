import scrapy


class CameraspiderSpider(scrapy.Spider):
    name = 'cameraspider'
    start_urls = [
        'https://www.jessops.com/cameras?fh_start_index=0&fh_view_size=21',
    ]
   # allowed_domains = ['https://www.jessops.com/cameras']
    #start_urls = ['https://www.jessops.com']

    def parse(self, response):
        camera = response.css('div.details-pricing')

        for cam in camera:
            items = {
                "Camera link" : cam.css('a::attr(href)').get(),
                "Camera name" : cam.css('a::text').get(),
                "Camera price" : cam.css('p.price.larger::text').get()
            }

            yield items

        
        cont = response.css('ul.f-pagination.f-margin-large-top')
        #next_page = cont.css('li').getall()[8]
        link = cont.css('li')[8]
        next_page = link.css('a::attr(href)').get()
        if next_page is not None:
            #yield response.follow(next_page, callback=self.parse)
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
     