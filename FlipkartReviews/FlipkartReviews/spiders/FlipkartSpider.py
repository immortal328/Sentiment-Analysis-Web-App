# -*- coding: utf-8 -*-
import scrapy
from scrapy.crawler import CrawlerProcess
import scrapy.crawler as crawler
from multiprocessing import Process, Queue
from twisted.internet import reactor
import pandas as pd


#output = {'Review': [], 'Sub-Review': []}


class FlipkartSpider(scrapy.Spider):
    output = {'Review': [], 'Sub-Review': []}
    name = 'Flipkart'
    to_df = False

    file = open("url.txt", "r")
    url = file.read()
    url = str(url)
    file.close()
    start_urls = [url
                  #'https://www.flipkart.com/dear-stranger-know-you-feel-journey-hope-healing/p/itm47dc1fa34daa0?pid=9789388754798&lid=LSTBOK9789388754798D1MDRQ&marketplace=FLIPKART&srno=s_1_1&otracker=search&otracker1=search&fm=SEARCH&iid=d11c11d2-ea24-40de-b8ae-c516e7070177.9789388754798.SEARCH&ppt=sp&ppn=sp&ssid=vsjx8vl7cg0000001586942952585&qH=7d8949bcbf85067f'
                  #'https://www.flipkart.com/eg-store-color-block-men-round-neck-grey-t-shirt/p/itm0534a077dd6e0?pid=TSHFEJWYH7Y9SAKJ&lid=LSTTSHFEJWYH7Y9SAKJRNUHE3&marketplace=FLIPKART&srno=s_1_2&otracker=AS_Query_TrendingAutoSuggest_7_0_na_na_na&otracker1=AS_Query_TrendingAutoSuggest_7_0_na_na_na&fm=SEARCH&iid=60eebfc0-a930-4ad5-af53-13c0ef46291d.TSHFEJWYH7Y9SAKJ.SEARCH&ppt=sp&ppn=sp&ssid=rtxiyx7dfy3tdzwg1586929074245&qH=04ad3bdbbe706182'
                  #'https://www.flipkart.com/lenovo-ideapad-s145-apu-dual-core-a6-4-gb-1-tb-hdd-windows-10-home-s145-15ast-thin-light-laptop/p/itmb227f905056eb?pid=COMFMHWEKBP4TBGJ&fm=organic&ppt=dynamic&ppn=dynamic&ssid=zyl2z79h8w0000001586935137673'
                  ]
    page_number = 0
    all_reviews_link = ''

    def parse(self, response):
        titles = response.css('._2xg6Ul')
        reviews = response.css('.qwjRop div')

        if titles == []:
            titles = response.css('._2t8wE0')
            reviews = []

        for t in titles:
            title = t.css('::text').extract_first()
            FlipkartSpider.output['Review'].append(title)

        if reviews != []:
            for r in range(0, len(reviews), 2):
                review = reviews[r].css('::text').extract_first()
                FlipkartSpider.output['Sub-Review'].append(review)
        yield{}

        if FlipkartSpider.page_number == 1:
            # Find all reviews button and get all reviews link
            FlipkartSpider.all_reviews_link = response.xpath(
                '//div[contains(@class, "col") and contains(@class, "_39LH-M")]').css('a::attr(href)')[-1].get()
            FlipkartSpider.output['Review'] = []
            FlipkartSpider.output['Sub-Review'] = []

        if FlipkartSpider.page_number == 0:
            # Get user input
            file = open("url.txt", "r")
            url = file.read()
            file.close()
            next_page = str(url)
            FlipkartSpider.output['Review'] = []
            FlipkartSpider.output['Sub-Review'] = []
        else:
            next_page = 'https://www.flipkart.com' + FlipkartSpider.all_reviews_link + \
                '&page=' + str(FlipkartSpider.page_number)

        # Scrawl part
        if response.css('._2xg6Ul') != [] or response.css('._2t8wE0') != []:
            FlipkartSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)
        else:
            FlipkartSpider.to_df = True
        # Scrawl part ends

        if FlipkartSpider.to_df:
            if FlipkartSpider.output['Sub-Review'] != []:
                df = pd.DataFrame.from_dict(FlipkartSpider.output)
            else:
                df = pd.DataFrame(
                    FlipkartSpider.output['Review'], columns=['Review'])
            df.to_csv('dataframe.csv', index=False, sep='|')


def run_spider(spider):
    def f(q):
        try:
            runner = crawler.CrawlerRunner()
            deferred = runner.crawl(spider)
            deferred.addBoth(lambda _: reactor.stop())
            reactor.run()
            q.put(None)
        except Exception as e:
            q.put(e)

    q = Queue()
    p = Process(target=f, args=(q,))
    p.start()
    result = q.get()
    p.join()

    if result is not None:
        raise result

#process = CrawlerProcess()
