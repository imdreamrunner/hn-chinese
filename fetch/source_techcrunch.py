# -*- coding: utf8 -*-
import logging
from .source_base import Origin
__author__ = "imdreamrunner"
__email__ = "imdreamrunner@gmail.com"

ORIGIN_NAME = "TechCrunch"


log = logging.getLogger(__name__)

title_list = "ul#river1 h2.post-title a"
title_css = "h1.alpha"
content_css = "div.article-entry.text"
image_css = "div.article-entry.text img"


class TechCrunch(Origin):
    def _list_page_url(self, page_number):
        if page_number == 1:
            return "http://techcrunch.com/"
        else:
            return "http://techcrunch.com/page/" + str(page_number) + "/"


origin = TechCrunch("TechCrunch", title_list, title_css, content_css, image_css)
