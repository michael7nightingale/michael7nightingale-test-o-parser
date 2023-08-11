from abc import abstractmethod, ABC
import time
from multiprocessing.pool import ThreadPool
from typing import Generator

from bs4 import Tag, BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class IContentManager(ABC):

    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class BaseParser(IContentManager):

    @classmethod
    def get_children_tags(cls, __tag: Tag) -> Generator[Tag, None, None]:
        for children_element in __tag.findChildren(recursive=False):
            if isinstance(children_element, Tag):
                yield children_element

    @classmethod
    def _initialize_driver(cls):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        ua = UserAgent()
        user_agent = ua.random
        options.add_argument(f'--user-agent={user_agent}')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        return driver

    def get_page_source(self, __url: str) -> str:
        if not hasattr(self, "driver"):
            raise AttributeError(f"{self} has not attribute driver, may be you forgot to user context manager?")
        self.driver.get(__url)
        time.sleep(2)
        return self.driver.page_source

    @classmethod
    def get_soup_from_page_source(cls, __page_source: str) -> BeautifulSoup:
        return BeautifulSoup(__page_source, "lxml")

    @classmethod
    def build_url(cls, url: str, **kwargs):
        query_string = "?" + '&'.join(f"{k}={v}" for k, v in kwargs.items())
        return url + query_string

    def __enter__(self):
        self.driver = self._initialize_driver()
        self.pool = ThreadPool()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.close()
