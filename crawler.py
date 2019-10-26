import logging
import time
import re
from typing import Dict, Optional

from bs4 import BeautifulSoup
from selenium import webdriver

logger = logging.getLogger(__name__)


class NewsCrawler:
    URL = "https://sports.news.naver.com/esports/news/index.nhn?isphoto=N"
    driver = None

    @classmethod
    def get_news(cls) -> Dict[str, str]:
        try:
            options = webdriver.ChromeOptions()
            options.headless = True
            options.no_sandbox = True
            options.disable_dev_shm_usage = True
            cls.driver = webdriver.Chrome("/home/ubuntu/chromedriver", options=options)
            cls.driver.implicitly_wait(3)
            cls.driver.get(cls.URL)
            return cls._news_crawling()

        except Exception:
            cls.driver.quit()
            logger.exception("")

    @classmethod
    def _news_crawling(cls) -> Optional[Dict[str, str]]:
        news_dict: Dict[str, str] = {}

        cls.driver.find_element_by_xpath("//li[@data-id='lol']/a").click()
        cls.driver.implicitly_wait(3)
        time.sleep(1)

        cls.driver.find_element_by_xpath("//li[@data-id='popular']/a").click()
        cls.driver.implicitly_wait(3)
        time.sleep(1)

        news_count = len(cls.driver.find_elements_by_xpath("//div[@class='news_list']/ul/li"))

        loop = 5
        if news_count < 5:
            loop = news_count

        for i in range(loop):
            cls._lol_popular(i + 1)

            soup = BeautifulSoup(cls.driver.page_source, 'html.parser')

            title = str(soup.find("h4").text)
            body_text = str(soup.find(id="newsEndContents").text)
            body_text = re.sub(r"(\n)|(\r)|(\s\s)", "", body_text)

            news_dict[title] = body_text

            cls.driver.back()
            cls.driver.implicitly_wait(3)
            time.sleep(2)

        cls.driver.quit()
        return news_dict

    @classmethod
    def _lol_popular(cls, i: int):
        cls.driver.find_element_by_xpath("//li[@data-id='lol']/a").click()
        cls.driver.implicitly_wait(3)
        time.sleep(1)

        cls.driver.find_element_by_xpath("//li[@data-id='popular']/a").click()
        cls.driver.implicitly_wait(3)
        time.sleep(1)

        cls.driver.find_element_by_xpath(f"//div[@class='news_list']/ul/li[{i}]/a").click()
        cls.driver.implicitly_wait(3)
        time.sleep(2)
