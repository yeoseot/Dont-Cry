import logging
import time
import re
from typing import Dict, Optional
from datetime import datetime

from bs4 import BeautifulSoup
from selenium import webdriver

from letter import chunk_and_send_message

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
        elements = cls.driver.find_elements_by_xpath('//li[@class="num1"]/dl/dt/a')

        for i in range(len(elements)):
            cls.driver.find_elements_by_xpath('//li[@class="num1"]/dl/dt/a')[i].click()
            soup = BeautifulSoup(cls.driver.page_source, 'html.parser')

            title = str(soup.find(id='articleTitle').text)
            body_text = str(soup.find(id='articleBodyContents').text)
            body_text = re.sub(r"(\s\s)+", "\n", body_text)

            time.sleep(1)
            cls.driver.back()
            time.sleep(1)
            news_dict[title] = body_text

        cls.driver.quit()
        return news_dict


if __name__ == '__main__':
    now = datetime.now()

    nc = NewsCrawler()
    news = nc.get_news()

    print(f'Parsed news count: {len(news)}')

    for i, news_data in enumerate(news.items()):
        index = i + 1
        news_title, news_content = news_data

        title = f'{now.strftime("%m/%d")} {index}번째 뉴스입니다.'
        content = f'제목: {news_title}\n내용: {news_content}'

        chunk_and_send_message(title, content)
