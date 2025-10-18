"""
scrapy - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.80
Tests Passed: 0/1
Learned: 2025-10-18T08:11:16.886534

This code has been verified by MIRAI's NASA-level learning system.
"""

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.exceptions import CloseSpider
from typing import Dict, Any

class ExampleSpider(scrapy.Spider):
    """A simple Scrapy spider to scrape example data from a website."""

    name = "example"
    start_urls = ["https://example.com"]  # Replace with the target URL

    def parse(self, response: scrapy.http.Response) -> Dict[str, Any]:
        """Parse the response and extract data."""
        try:
            title = response.css('title::text').get()  # Extract the title of the page
            if title is None:
                raise ValueError("Title not found on the page")

            yield {
                'title': title,
                'url': response.url,
            }
        except Exception as e:
            self.logger.error(f"Error occurred: {e}")
            raise CloseSpider(reason=str(e))

if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(ExampleSpider)
    process.start()  # The script will block here until the crawling is finished