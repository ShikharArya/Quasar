import scrapy
import numpy as np
import pickle

class BlogSpider(scrapy.Spider):
    name = 'quasar'
    start_urls = ["https://en.wikipedia.org/wiki/Galactic_Center#Gamma-_and_X-ray_emitting_Fermi_bubbles", "https://en.wikipedia.org/wiki/Crab_Nebula", "https://en.wikipedia.org/wiki/Coalsack_Nebula", "https://en.wikipedia.org/wiki/Horsehead_Nebula"]
    def parse(self, response):
        with open("./data/" + response.url.split("/")[-1] + ".txt", "wb") as f:
            f.write(np.char.replace(' '.join(response.css("p::text, p *::text").extract()).encode("utf-8"), "\n", ""))
            f.close()

        # links = []
        # for link in links:
        #     yield response.follow(link, callback=parse)

        # for title in response.css('h2'):
        #     yield {'title': title.css('span ::text').get()}
        #     print("\n")

        # for data in response.css('p'):
        #     yield {'data': data.css('p ::text').get()}  
        #     print("\n")  

        #yield {
        #    "links" : ["https://en.wikipedia.org" + link for link in response.css('.mw-category-group a').css("::attr(href)").extract()]
        #}