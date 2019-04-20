# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import scrapy

class JArchiveSpider(scrapy.Spider):
    name = "JArchive"

    def start_requests(self):
        urls =  ["https://j-archive.com/showseason.php?season="  + str(x) for x in range(1,35)]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        season= response.url.split("=")[1]
        filename = 'season-%s.html' % season
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

        games = response.css('div#content table td a::attr(href)').getall()
        games = filter( lambda a : 'game_id' in a, games)

        for game in games:
            yield response.follow(url=game, callback=self.parse_game)

    def parse_game(self, response):
        game= response.url.split("=")[1]
        filename = 'game-%s.html' % game
        with open(filename, 'w') as f:
            f.write(response.css('div#content').get())
        self.log('Saved file %s' % filename)
