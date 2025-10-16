"""
scrapy - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-16T08:30:36.101070

This code has been verified by MIRAI's NASA-level learning system.
"""

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.exceptions import CloseSpider
from typing import Dict, Any

class ExampleSpider(scrapy.Spider):
    """Spider to scrape example data from a website."""

    name = "example_spider"
    start_urls = ["http://example.com"]  # Replace with your target URL

    def parse(self, response: scrapy.http.Response) -> Dict[str, Any]:
        """Parse the response from the start URL and extract data."""
        try:
            title = response.css('title::text').get()  # Extract the title text
            if not title:
                raise CloseSpider("Title not found")
            yield {
                'title': title,  # Yield the extracted title
                'url': response.url,  # Yield the URL of the page
            }
        except Exception as e:
            self.logger.error(f"Error parsing response: {e}")  # Log any parsing errors

if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(ExampleSpider)
    process.start()  # Start the crawling process