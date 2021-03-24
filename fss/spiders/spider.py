import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import FssItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class FssSpider(scrapy.Spider):
	name = 'fss'
	start_urls = ['https://www.fssbank.com/accounts/about-us/news']

	def parse(self, response):
		post_links = response.xpath('//h2/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		date = response.xpath('//div[@class="post-list-byline"]/text()').get().split('by')[0].strip()
		title = response.xpath('(//h1)[2]/span/text()').get()
		content = response.xpath('//section[@class="main-content"]/div//div[2]//text()').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=FssItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
