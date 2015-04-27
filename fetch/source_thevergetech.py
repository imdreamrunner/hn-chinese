# -*- coding: utf8 -*-
import logging
from .source_base import Origin
__author__ = "imdreamrunner"
__email__ = "imdreamrunner@gmail.com"

ORIGIN_NAME = "TechCrunch"


log = logging.getLogger(__name__)


title_list = "li.p-basic-article-list__node h3 a"
title_css = "h1#stream_title"
content_css = "div.m-article__entry"
image_css = "div.m-article__entry-section div.p-dynamic-image"


class TheVergeTech(Origin):
    def _list_page_url(self, page_number):
        if page_number == 1:
            return "http://www.theverge.com/tech/archives"
        else:
            return "http://www.theverge.com/tech/archives/" + str(page_number)


origin = TheVergeTech("TheVergeTech", title_list, title_css, content_css, image_css)
