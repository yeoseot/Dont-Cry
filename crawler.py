import logging
import time
import re
from typing import Dict, Optional
from datetime import datetime

from bs4 import BeautifulSoup
from selenium import webdriver

from letter import send_message

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
            cls.driver = webdriver.Chrome("./chromedriver", options=options)
            cls.driver.implicitly_wait(10)
            cls.driver.get(cls.URL)
            return cls._news_crawling()

        except Exception:
            cls.driver.quit()
            logger.exception("")

    @classmethod
    def _news_crawling(cls) -> Optional[Dict[str, str]]:
        news_dict: Dict[str, str] = {}

        cls.driver.find_element_by_xpath("//li[@data-id='lol']/a").click()
        time.sleep(0.5)

        cls.driver.find_element_by_xpath("//li[@data-id='popular']/a").click()
        time.sleep(0.5)

        news_count = len(cls.driver.find_elements_by_xpath("//div[@class='news_list']/ul/li"))

        loop = 5
        if news_count < 5:
            loop = news_count

        for i in range(loop):
            cls._lol_popular(i + 1)

            soup = BeautifulSoup(cls.driver.page_source, 'html.parser')

            title = str(soup.find("h4").text)
            body_text = str(soup.find(id="newsEndContents").text)
            body_text = re.sub(r"(\n)|(\r)|(\s\s)", "    ", body_text)

            news_dict[title] = body_text

            cls.driver.back()
            time.sleep(1)
        cls.driver.quit()
        return news_dict

    @classmethod
    def _lol_popular(cls, i: int):
        cls.driver.find_element_by_xpath("//li[@data-id='lol']/a").click()
        time.sleep(0.5)

        cls.driver.find_element_by_xpath("//li[@data-id='popular']/a").click()
        time.sleep(0.5)

        cls.driver.find_element_by_xpath(f"//div[@class='news_list']/ul/li[{i}]/a").click()
        time.sleep(1)


if __name__ == '__main__':
    now = datetime.now()

    nc = NewsCrawler()
    news = nc.get_news()

    print(f'Parsed news count: {len(news)}')

    for i, news_data in enumerate(news.items()):
        index = i + 1
        news_title, news_content = news_data

        title = f'{now.strftime("%Y년 %m월 %d일")} e스포츠 LOL 인기순 TOP5 {index}번째 뉴스입니다.'
        content = f'제목: {news_title}\n내용: {news_content}'
        send_message(title, content)
