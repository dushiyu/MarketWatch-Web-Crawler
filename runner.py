import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from marketwatch.spiders.latest import LatestSpider

process = CrawlerProcess(settings=get_project_settings())
process.crawl(LatestSpider)
process.start()