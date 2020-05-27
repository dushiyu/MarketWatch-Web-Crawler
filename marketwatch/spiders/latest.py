# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
import pdb

class LatestSpider(scrapy.Spider):
    name = 'latest'
    allowed_domains = ['www.marketwatch.com']
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'

    # LUA script to all pages 
    # by clicking "See More" botton until webpage length doesn't change
    lua_script_pagination = '''
        function main(splash, args)
            splash.private_mode_enabled = false

            url = args.url
            assert(splash:go(url))
            assert(splash:wait(1))

            see_more_btn = assert(splash:select_all(".js--more-headlines"))
            local web_length = 0

            while #splash:html() > web_length do
                web_length = #splash:html()
                see_more_btn[1]:mouse_click()
                assert(splash:wait(1))
            end

            splash:set_viewport_full()
            return splash:html()
        end
    '''

    # LUA script for log in the website
    lua_script_login = '''
        function main(splash, args)
            splash.private_mode_enabled = false
            url = args.url
            assert(splash:go(url))
            assert(splash:wait(1))

            input_username = assert(splash:select("#username"))
            input_username:focus()
            input_username:send_text('%s')
            assert(splash:wait(0.5))

            input_username = assert(splash:select("#password"))
            input_username:focus()
            input_username:send_text('%s')
            assert(splash:wait(0.5))

            btn = assert(splash:select(".basic-login-submit"))
            btn:mouse_click()
            assert(splash:wait(5))

            splash:set_viewport_full()
            return splash:html()
        end
    '''
  
    def start_requests(self):
        # try to login if username and password are set
        try:
            login_script = self.lua_script_login%(DOWJONES_USERNAME,DOWJONES_PASSWORD)
            yield SplashRequest(url='https://accounts.marketwatch.com/login?target=https%3A%2F%2Fwww.marketwatch.com%2F', 
                callback=self.after_login, 
                endpoint="execute", 
                headers={'User-Agent': self.user_agent},
                args={'lua_source': login_script},
            )
        # go ahead with pagination if not logging in
        except NameError:
            yield SplashRequest(url="https://www.marketwatch.com/latest-news", 
            callback=self.parse, 
            endpoint="execute", 
            headers={'User-Agent': self.user_agent},
            args={'lua_source': self.lua_script_pagination}, 
        )
        
    def after_login(self,response):
        print('Logged in...')
        yield SplashRequest(url="https://www.marketwatch.com/latest-news", 
            callback=self.parse, 
            endpoint="execute", 
            headers={'User-Agent': self.user_agent},
            args={'lua_source': self.lua_script_pagination},
        )

    def parse(self, response):
        # get all article links from headline page
        articles = response.xpath('//div[@data-layout-position="1.1"]//div[contains(@class,"article__content")]')

        for article in articles:
            link = article.xpath('./h3//@href').get()
            meta_data = {
                'label': article.xpath('normalize-space(./span/text())').get(),
                'headline': article.xpath('.//h3[contains(@class,"article__headline")]').xpath('normalize-space(.)').get(),
                'article_summary': article.xpath('./p//text()').get(),
                'timestamp': article.xpath('./div[contains(@class,"article__details")]//@data-est').get(),
            }

            # two types of headlines: 
            # 1) flash news without full article link -> output headline
            # 2) articles with a link -> scrape the article web
            if link:
                yield response.follow(url=link, callback=self.parse_article, meta=meta_data)
            else:
                meta_data['label'] = 'flash headline'
                yield {
                    'frontpage_summary': meta_data
                }

    def parse_article(self, response):
        # parse articles from 
        meta = response.request.meta
        category = response.xpath('//li[@class="breadcrumb__item"]/a/text()').getall()[1:]
        header = response.xpath('//div[@class="article__masthead"]')
        referenced_tickers = response.xpath('//div[contains(@class,"referenced-tickers")]//a[contains(@class,"qt-chip-referenced link")]')
        content = response.xpath('//div[contains(@class," column--full article__content")]')
        
        yield{
            'frontpage_summary': {
                'url': response.url,
                'headline': meta['headline'],
                'article_summary': meta['article_summary'],
                'label': meta['label'],
            },
            'category': category,
            'header': {
                'headline': header.xpath('normalize-space(./h1/text())').get(),
                'sub_headline': header.xpath('normalize-space(./h2[contains(@class,"article__subhead")]/text())').get(),
                'time_publish': header.xpath('normalize-space(./time[contains(@class,"timestamp--pub")]/text())').get(),
                'time_update': header.xpath('normalize-space(./time[contains(@class,"timestamp--update")]/text())').get(),
            },
            'author': {
                'author_name': header.xpath('.//div[contains(@class,"author")]//h4//text()').get(),
                'author_link': header.xpath('.//div[contains(@class,"author")]//@href').get(),
            },
            'referenced_tickers': {
                item.xpath('.//span[@class="symbol"]/text()').get(): item.xpath('normalize-space(.//bg-quote//text())').get() for item in referenced_tickers
            },
            'paragraphs': content.xpath('.//p').xpath('normalize-space(.)').getall(),
            'related_articles': content.xpath('.//p//@href').getall(),
        }
            
