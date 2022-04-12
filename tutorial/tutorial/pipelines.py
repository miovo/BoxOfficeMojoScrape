# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import csv

class MoviePipeline():

    def __init__(self):
        self.csvwriter = csv.writer(open("MovieInfo.csv", "w", newline=''))
        self.csvwriter.writerow(["Year", "Movie Title", "Distributor",  "Gross Revenue", "Theaters", "Release Date"])

    def process_item(self, item, spider):
        row = []
        row.append(item["year"])
        row.append(item["title"])
        row.append(item["distributor"])
        row.append(item["gross_rev"])
        row.append(item["theaters"])
        row.append(item["release_date"])

        self.csvwriter.writerow(row)

        return item

    def close_spider(self, spider):
        print("Done")
