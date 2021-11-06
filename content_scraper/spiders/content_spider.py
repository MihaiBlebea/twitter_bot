from scrapy import Request, Spider
from scrapy_splash import SplashRequest
import json


class ContentSpider(Spider):

	name = "content"

	start_urls = [
		"https://hackernoon.com/search?query=golRequestang"
	]

	def start_requests(self):
		for url in self.start_urls:
			yield SplashRequest(
				url, 
				callback=self.parse_articles_page,
				args={
					"wait": 10
				}
			)

	def parse_articles_page(self, response):
		# yield {
		# 	"page": response.text
		# }
		articles = response.css("article").getall()
		for article in articles:
			title = article.css("h2.a::text").get()
			yield {
				"title": title
			}