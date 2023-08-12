import re
import time
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup, Tag
from typing import Generator

from .base import BaseParser


class OzoneProductsParser(BaseParser):
    STEPS_TO_GOOD_LIST = (1, 7, 1, 1, 2, 3, 1, 1, 1)
    ID_PATTERN = re.compile(r"/product/.*?(\d*)/")

    def __init__(self, base_url: str, max_pages: int):
        self.base_url = base_url
        self.max_pages = max_pages

    def find_goods_list_tag(self, soup: BeautifulSoup) -> Tag:
        initial_element = soup.find("div", {"id": "layoutPage"})
        if initial_element is None:
            raise ValueError("Could not find page layout!")
        element = initial_element
        for step in self.STEPS_TO_GOOD_LIST:
            for idx, ch in enumerate(self.get_children_tags(element), 1):
                if idx == step:
                    element = ch
                    break
        return element

    def get_goods(self, tag: Tag) -> Generator[dict, None, None]:
        for good_tag in self.get_children_tags(tag):
            good = {}
            try:
                a_tag, div_tag, _ = self.get_children_tags(good_tag)
            except ValueError:
                continue
            url = a_tag["href"]
            img_tag = next(next(next(a_tag.children).children).children)
            good['image_url'] = img_tag['src']
            good['url'] = url
            id_ = self.ID_PATTERN.findall(url)[0]

            div_price, a_info, *_ = self.get_children_tags(div_tag)
            div_price = next(div_price.children)
            total_span, price_span, discount_span = self.get_children_tags(div_price)
            title_span = next(next(a_info.children).children)

            good['name'] = title_span.text
            good['id'] = id_
            price = price_span.text.replace("\u2009", "").replace("₽", "")
            if price and price.isnumeric():
                good['price'] = int(price)
            else:
                continue
            discount = discount_span.text.replace("−", "").replace("%", "")
            good['discount'] = int(discount) if discount and discount.isnumeric() else 0

            yield good

    def parse(self, page) -> Generator[dict, None, None]:
        try:
            page_source = self.get_page_source(self.build_url(self.base_url, page=page))
            soup = self.get_soup_from_page_source(page_source)
            goods_list_tag = self.find_goods_list_tag(soup)
            goods_gen = self.get_goods(goods_list_tag)
            return goods_gen
        except Exception as e:
            return ({} for i in range(0))

    def __call__(self):
        goods_generators = self.pool.map_async(self.parse_multi_drivers, range(1, self.max_pages + 1))
        goods_generators.wait()
        return goods_generators.get()

    def parse_multi_drivers(self, page):
        driver = None
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            ua = UserAgent()
            user_agent = ua.random
            options.add_argument(f'--user-agent={user_agent}')
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            url = self.build_url(self.base_url, page=page)
            driver.get(url)
            time.sleep(2)
            soup = BeautifulSoup(driver.page_source, "lxml")
            goods_list_dev = self.find_goods_list_tag(soup)
            goods = self.get_goods(goods_list_dev)
            return_ = goods
        except Exception as e:
            return_ = iter([{}])
        if driver is not None:
            driver.close()
        return return_


if __name__ == '__main__':
    # with OzoneProductsParser(base_url="https://www.ozon.ru/seller/proffi-1/products", max_pages=4) as parser:
    #     result = parser()
    #     for good_party in result:
    #         for good in good_party:
    #             print(good)
    ...
