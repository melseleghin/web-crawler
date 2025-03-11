import scrapy
from pymongo import MongoClient

MONGO_URI = "mongodb+srv://melseleghin:Morangu!nh0@brands.tr5lj.mongodb.net"
DATABASE_NAME = "web_crawler"
COLLECTION_DATA = "brands"

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]

class BrandsSpider(scrapy.Spider):
    name = "brands"
    start_urls = [
        "https://www.rankingthebrands.com/The-Brands-and-their-Rankings.aspx",
    ]
    all_brands = []

    def parse(self, response):
        data_to_insert = []
        for brand in response.css("div#ctl00_mainContent_brandPanel div.brandLine"):
            data_to_insert.append({"Brand": brand.css("span.rankingName::text").get()})
            self.all_brands.append(brand.css("span.rankingName::text").get())
            yield {
                "Brand": brand.css("span.rankingName::text").get()
            }

        # Coleta os links das letras (A-Z)
        next_letters = response.css("div#ctl00_mainContent_filterPanel a::attr(href)").getall()
        for letter_link in next_letters:
            yield response.follow(letter_link, callback=self.parse)

        # db[COLLECTION_DATA].insert_many(data_to_insert)

    def closed(self, reason):
        if self.all_brands:
            db[COLLECTION_DATA].insert_one({"All_Brands": self.all_brands})