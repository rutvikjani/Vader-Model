import scrapy
import pandas as pd;
from scrapy import Request

class ArticlespiderSpider(scrapy.Spider):
                name = "articlespider"
                allowed_domains = ["website url"]

                def start_requests(self):    
                    df = pd.read_csv(r'D:\python\scrapy\articlescraper\data.csv')    
                    for _, rows in df.iterrows():
                        start_urls = rows['URL']
                        yield scrapy.Request(url=start_urls, callback=self.parse, meta={'row_data':rows})
                        


                def parse(self, response):
                    row_data = response.meta['row_data']
                    # file_name = row_data['URL_ID']
                    file_path = r"D:\python\scrapy\articlescraper\extracted data\{}.txt".format(row_data['URL_ID'])
                    heading = response.css("h1::text").get(),
                    paragraph = response.css("p::text").getall()
                    with open(file_path, "w+", encoding='utf-8') as file:
                        file.write(f"{heading} \n")
                        file.write(f"{paragraph}")    


        