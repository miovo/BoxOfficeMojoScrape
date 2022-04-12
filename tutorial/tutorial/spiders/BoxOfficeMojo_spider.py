



import scrapy

from ..items import MovieInfo

class MojoSpider(scrapy.Spider):

    name = "mojo"

    start_urls = [
      #"https://www.boxofficemojo.com/year/2000",
      #"https://www.boxofficemojo.com/year/2001",
      "https://www.boxofficemojo.com/year/2002",
      #"https://www.boxofficemojo.com/year/2003",
      #"https://www.boxofficemojo.com/year/2004",
      #"https://www.boxofficemojo.com/year/2005",
      #"https://www.boxofficemojo.com/year/2006",
      #"https://www.boxofficemojo.com/year/2007",
      #"https://www.boxofficemojo.com/year/2008",
      #"https://www.boxofficemojo.com/year/2009",
      #"https://www.boxofficemojo.com/year/2010"
    ]

    def parse(self, response):
                                                            #THIS IS WHAT SAYS HOW MANY TIMES TO LOOP
                                                            #Set to [1:201] to loop to the end of each list (200 per list)
        for tr in response.xpath('//*[@id="table"]/div/table/tr')[1:20]:
            href = tr.xpath('./td[2]/a/@href')
            url = response.urljoin(href[0].extract())
            yield scrapy.Request(url, callback=self.parse_page_contents)

    def parse_page_contents(self, response):
        item = MovieInfo()

        #Special Cases
        item["title"] = response.xpath('//*[@id="a-page"]/main/div/div[1]/div[1]/div/div/div[2]/h1/text()')[0].extract()
        item["gross_rev"] = response.xpath('//*[@id="a-page"]/main/div/div[3]/div[1]/div/div[1]/span[2]/span/text()')[0].extract()

        elements = []
        for div in response.xpath('//*[@id="a-page"]/main/div/div[3]/div[4]/div')[0:]:
            elements.append(' '.join(div.xpath('./span[1]/text()')[0].extract().split()))

        #Distributor
        if 'Distributor' in elements:
            d = elements.index('Distributor') + 1
            loc_dist = '//*[@id="a-page"]/main/div/div[3]/div[4]/div[{}]/span[2]/text()'.format(d)
            item["distributor"] = response.xpath(loc_dist)[0].extract()
        else:
            item["distributor"] = "N/A"

        # Opening Theaters
        if 'Opening' in elements:
           o = elements.index('Opening') + 1
           loc_open_theater = '//*[@id="a-page"]/main/div/div[3]/div[4]/div[{}]/span[2]/text()'.format(o)
           try:
               item["theaters"] = response.xpath(loc_open_theater)[0].extract().split()[0]
           except:
               item["theaters"] = "N/A"
        else:
            item["theaters"] = "N/A"

        #Release Date with Year and parse out of Year (seperate)
        #There is a date range for most, Just pull the first date
        if 'Release Date' in elements:
            r = elements.index('Release Date') + 1
            loc_release = '//*[@id="a-page"]/main/div/div[3]/div[4]/div[{}]/span[2]/a/text()'.format(r)
            item["release_date"] = response.xpath(loc_release)[0].extract()
            #Remote the date and grab the year
            item["year"] = response.xpath(loc_release)[0].extract().split(",")[-1]

        #Some are different and use "Release Date (Wide)", Accomidate for that here by grabbing the first date
        elif 'Release Date (Wide)' in elements:
            r = elements.index('Release Date (Wide)') + 1
            loc_release = '//*[@id="a-page"]/main/div/div[3]/div[4]/div[{}]/span[2]/a/text()'.format(r)
            item["release_date"] = response.xpath(loc_release)[0].extract()
            #Remove the date and grab the year
            item["year"] = response.xpath(loc_release)[0].extract().split(",")[-1]
        else:
            item["release_date"] = "N/A"
            item["year"] = "N/A"

            
        yield item
 