import logging
import store
from . import fetch_util
from bs4 import BeautifulSoup

__author__ = "imdreamrunner"
__email__ = "imdreamrunner@gmail.com"

log = logging.getLogger(__name__)


class Origin:
    def __init__(self, name, title_list, title_css, content_css, image_css):
        self.ORIGIN_NAME = name
        self.title_list = title_list
        self.title_css = title_css
        self.content_css = content_css
        self.image_css = image_css

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
        titles = soup.select(self.title_list)
        url_list = list()
        for title in titles:
            try:
                url_list.append(title["href"])
            except Exception as e:
                log.info("Error getting link:" + e)
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
        title = soup.select(self.title_css)
        if len(title) > 0:
            title = title[0]
            title = title.text.encode('utf-8').strip()
        content = soup.select(self.content_css)
        if len(content) > 0:
            content = content[0]
            content = content.text.encode('utf-8').strip()
        else:
            content = None
        image = soup.select(self.image_css)
        if len(image) > 0:
            image = image[0]
            if image.has_attr("src") and len(image["src"]) > 0:
                image = image['src'].encode('utf-8')
            elif image.has_attr("data-original") and len(image["data-original"]) > 0:
                image = image['data-original'].encode('utf-8')
            else:
                log.debug(image)
                image = None
                raise
        else:
            image = None
        log.info(title)
        log.info(content)
        log.info(image)
        return title, content, image