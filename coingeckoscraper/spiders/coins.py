import logging
import time

import scrapy
from scrapy.exceptions import CloseSpider
from scrapy.http import HtmlResponse, Request
from scrapy.loader import ItemLoader
from scrapy.selector import Selector

from coingeckoscraper.items import GeckoCoin

logger = logging.getLogger(__name__)


class CoinsSpider(scrapy.Spider):
    name = "coins"
    allowed_domains = ["www.coingecko.com", "coingecko.com"]

    pages_to_parse = 1
    items_size = 300

    BASE_URL = "https://www.coingecko.com"
    __COINS_LINKS_XPATH = "//table[@data-page]/tbody/tr/td/a/@href"


    class CoinDetailsSelectors:
        RATING_SELECTOR = "span.tw-mt-0\.5:nth-child(3) > div:nth-child(1)::text"
        NAME_SELECTOR = "div.\!tw-text-base::text"
        PRICE_SELECTOR = ".tw-text-3xl > span:nth-child(1)::text"
        HOUR_CHANGE_SELECTOR = ()
        DAILY_VOLUME_XPATH = "/html/body/div[2]/main/div/div[2]/div[6]/div[2]/table/tbody/tr[4]/td/span/text()"
        MARKET_CAPITAL_XPATH = "/html/body/div[2]/main/div/div[2]/div[6]/div[2]/table/tbody/tr[1]/td/span/text()"
        PORTFOLIO_UPDATES_SELECTOR = "span.\!tw-font-normal::text"
        CHANGES_SELECTORS = {
            "HOUR_CHANGE_SELECTOR": "td.tw-text-center:nth-child(1) > span:nth-child(1)",
            "DAY_CHANGE_SELECTOR": "td.tw-text-center:nth-child(2) > span:nth-child(1)",
            "WEEK_CHANGE_SELECTOR": "td.tw-text-center:nth-child(3) > span:nth-child(1)",
            "TWO_WEEKS_CHANGE_SELECTOR": "td.tw-text-center:nth-child(4) > span:nth-child(1)",
            "MONTH_CHANGE_SELECTOR": "td.tw-text-center:nth-child(5) > span:nth-child(1)",
            "YEAR_CHANGE_SELECTOR": "td.tw-text-center:nth-child(6) > span:nth-child(1)",
        }


    def start_requests(self):
        for i in range(self.pages_to_parse):
            yield Request(f"{self.BASE_URL}/?page={i + 1}/&items={self.items_size}")


    def parse(self, response: HtmlResponse):
        if response.status == 404:
            raise CloseSpider("No next page found")

        for path in response.xpath(self.__COINS_LINKS_XPATH).getall():
            yield Request(self.BASE_URL + path, self.parse_item)


    def parse_item(self, response: HtmlResponse):
        def parse_changes(selector: Selector, change_queries: list[str]):

            def get_absolute_percentage(selector: Selector):
                change_direction = selector.attrib.get("class")
                if change_direction == None:
                    return "-"

                sign = "+" if "gecko-up" in change_direction else "-"
                return sign + selector.css("*::text").get()

            return [
                get_absolute_percentage(selector.css(query)) for query in change_queries
            ]

        yield GeckoCoin(
            response.css(self.CoinDetailsSelectors.RATING_SELECTOR).get().strip(),
            response.css(self.CoinDetailsSelectors.NAME_SELECTOR).get().strip(),
            response.css(self.CoinDetailsSelectors.PRICE_SELECTOR).get(),
            response.xpath(self.CoinDetailsSelectors.DAILY_VOLUME_XPATH).get(),
            response.xpath(self.CoinDetailsSelectors.MARKET_CAPITAL_XPATH).get(),
            response.css(self.CoinDetailsSelectors.PORTFOLIO_UPDATES_SELECTOR)
            .get()
            .strip(),
            *parse_changes(
                response.xpath("//body"),
                self.CoinDetailsSelectors.CHANGES_SELECTORS.values(),
            ),
            url=response.url,
        )

