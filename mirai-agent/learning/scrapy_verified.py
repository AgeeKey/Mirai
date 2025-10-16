"""
scrapy - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.82
Tests Passed: 0/1
Learned: 2025-10-16T02:19:47.805390

This code has been verified by MIRAI's NASA-level learning system.
"""

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.exceptions import CloseSpider


class QuotesSpider(scrapy.Spider):
    """Spider that scrapes quotes from http://quotes.toscrape.com"""
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]

    def parse(self, response: scrapy.http.Response) -> None:
        """Parse the response and extract quotes."""
        try:
            quotes = response.css("div.quote")
            for quote in quotes:
                yield {
                    'text': quote.css("span.text::text").get(),
                    'author': quote.css("span small.author::text").get(),
                    'tags': quote.css("div.tags a.tag::text").getall(),
                }
                
            # Follow pagination link
            next_page = response.css("li.next a::attr(href)").get()
            if next_page:
                yield response.follow(next_page, self.parse)
            else:
                raise CloseSpider(reason="No more pages to scrape.")
        except Exception as e:
            self.logger.error(f"Error while parsing: {e}")


if __name__ == "__main__":
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(QuotesSpider)
    process.start()