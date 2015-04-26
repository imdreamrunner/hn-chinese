# -*- coding: utf8 -*-
import os
import logging
import store
import shutil
import util.common
from . import _template, url

__author__ = "imdreamrunner"
__email__ = "imdreamrunner@gmail.com"


log = logging.getLogger(__name__)

HTML_BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../html"))
IMAGE_BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../images"))
PAGE_SIZE = 10


def generate():
    articles = store.get_row_by_status(4)
    page_number = 1
    page_start = 0
    index_template = _template.get_template("index")
    while page_start < len(articles):
        page_articles = articles[page_start: page_start+PAGE_SIZE]
        _write_to_file(url.index(page_number), index_template.render(articles=page_articles,
                                                                     page_current=page_number,
                                                                     page_total=(len(articles) - 1) / PAGE_SIZE + 1))
        page_start += PAGE_SIZE
        page_number += 1
    article_template = _template.get_template("article")
    tag_article = dict()
    for article in articles:
        for tag in article['tags'].split(","):
            if tag not in tag_article:
                tag_article[tag] = list()
            tag_article[tag].append(article)
        _write_to_file(url.article(article["id"]), article_template.render(article=article))
        if article["image"] is not None and len(article["image"]) > 0:
            _copy_images(article["image"])
    tag_list = sorted([{"tag": tag, "articles": article} for tag, article in tag_article.iteritems()], cmp=compare_tag)
    tag_template = _template.get_template("tag")
    for tag_item in tag_list:
        tag = tag_item["tag"]
        tag_articles = tag_item["articles"]
        page_number = 1
        page_start = 0
        while page_start < len(tag_articles):
            page_articles = tag_articles[page_start: page_start + PAGE_SIZE]
            _write_to_file(url.tag(tag, page_number),
                           tag_template.render(tag=tag,
                                               articles=page_articles,
                                               page_current=page_number,
                                               page_total=(len(page_articles) - 1) / PAGE_SIZE + 1))
            page_start += PAGE_SIZE
            page_number += 1



def compare_tag(tag_item_1, tag_item_2):
    if len(tag_item_1["articles"]) < len(tag_item_2["articles"]):
        return 1
    if len(tag_item_1["articles"]) > len(tag_item_2["articles"]):
        return -1
    return 0

def _write_to_file(filename, content):
    log.info("Generated " + filename + ".")
    if not os.path.exists(HTML_BASE_PATH):
        os.mkdir(HTML_BASE_PATH)
    with open(HTML_BASE_PATH + "/" + filename, "wb") as f:
        f.write(content.encode("utf-8"))


def _copy_images(url):
    if not os.path.exists(HTML_BASE_PATH + "/images"):
        os.mkdir(HTML_BASE_PATH + "/images")
    if os.path.exists(IMAGE_BASE_PATH + "/" + util.common.get_file_name(url)):
        shutil.copy(IMAGE_BASE_PATH + "/" + util.common.get_file_name(url),
                    HTML_BASE_PATH + "/images/" + util.common.get_file_name(url))
    else:
        log.error("Image file not found: " + util.common.get_file_name(url))