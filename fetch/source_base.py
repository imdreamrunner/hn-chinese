import logging
import store
from . import fetch_util
from bs4 import BeautifulSoup

__author__ = "imdreamrunner"
__email__ = "imdreamrunner@gmail.com"

log = logging.getLogger(__name__)


class Origin:
    def __init__(self, name):
        self.ORIGIN_NAME = name

    def fetch(self, limit):
        self._fetch_url(limit)
        self._fetch_articles()

    def _fetch_url(self, limit):
        page = 1
        count = 0
        while True:
            if count >= limit:
                return
            url = self._list_page_url(page)
            html = fetch_util.fetch_html(url)
            urls = self._get_url_list(html)
            # log.info("URL List: " + str(urls))
            page_count = 0
            for url in urls:
                if store.save_new_url(url, self.ORIGIN_NAME):
                    count += 1
                    page_count += 1
                    if count >= limit:
                        return
            page += 1
            if page_count == 0:
                return count

    def _get_url_list(self, html):
        if html is None:
            return list()
        soup = BeautifulSoup(html)
        titles = soup.select("ul#river1 h2.post-title")
        url_list = list()
        for title in titles:
            url_list.append(title.find("a")["href"])
        return url_list

    def _list_page_url(self, page_number):
        pass

    def _fetch_articles(self):
        urls = store.get_urls_by_status(self.ORIGIN_NAME, 0)
        for url in urls:
            html = fetch_util.fetch_html(url)
            title, content, image_url = self._process_article(html)
            if title is None or content is None:
                store.update_status(url, self.ORIGIN_NAME, 11)
                continue
            if image_url is not None:
                fetch_util.fetch_image(image_url)
            store.update_origin(url, self.ORIGIN_NAME, title, content, image_url)

    def _process_article(self, html):
        if html is None:
            return None, None, None
        soup = BeautifulSoup(html)
        [s.extract() for s in soup('script')]
        title = soup.select("h1.alpha")
        if len(title) > 0:
            title = title[0]
            title = title.text.encode('utf-8')
        content = soup.select("div.article-entry.text")
        if len(content) > 0:
            content = content[0]
            content = content.text.encode('utf-8')
        else:
            content = None
        image = soup.select("div.article-entry.text img")
        if len(image) > 0:
            image = image[0]
            image = image['src'].encode('utf-8')
        else:
            image = None
        return title, content, image