import csv
import time
import math
from selectorlib import Extractor
from bs4 import BeautifulSoup
from tqdm.auto import tqdm
from dateutil import parser as dateparser
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service

options = webdriver.FirefoxOptions()
options.headless = True
_browser = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
_extractor = Extractor.from_yaml_file('selectors.yml')


class AmazonReviewScraper:
    def __init__(self, asin, sleep=1, start_page=1, end_page=None):
        self.id = 1
        self.asin = asin
        self.url = f"https://www.amazon.com/dp/product-reviews/{asin}?pageNumber={{}}"
        self.sleep = sleep
        self.start_page = start_page
        self.end_page = end_page or self.total_pages()

    def fetch_webpage(self, url):
        _browser.get(url)
        html = _browser.page_source
        return html

    def total_pages(self):
        html = self.fetch_webpage(self.url.format(1))
        soup = BeautifulSoup(html, 'html.parser')
        review_count = soup.find_all("div", {"data-hook": "cr-filter-info-review-rating-count"})
        total_reviews = int(review_count[0].text.replace('\n', '')[46:51].replace(',', ''))
        return math.ceil(total_reviews / 10)

    def data_scraper(self, page, writer):
        url = self.url.format(page)
        html = self.fetch_webpage(url)
        data = _extractor.extract(html)
        if data:
            for review in data['reviews']:
                if not review:
                    continue
                review["ID"] = self.id
                self.id += 1
                review["Link"] = "https://www.amazon.com"+review.get("Link")
                review["Stars"] = float(review.get("Stars", 0).split(" out of")[0])
                date_posted = review.get("Date", "").split("on ")[-1]
                review["Date"] = dateparser.parse(date_posted).strftime("%d %b %Y")
                writer.writerow(review)

    def scrape(self):
        with open(f"{self.asin}.csv", "w", encoding="utf-8", newline="") as outfile:
            writer = csv.DictWriter(outfile, fieldnames=["ID", "Link", "User", "Date", "Stars", "Title", "Text"], quoting=csv.QUOTE_ALL)
            writer.writeheader()
            for page in tqdm(range(self.start_page, self.end_page + 1)):
                self.data_scraper(page, writer)
                time.sleep(self.sleep)


scraper = AmazonReviewScraper(asin='B000GAYQKY', sleep=0)
scraper.scrape()
