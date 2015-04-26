# -*- coding: utf8 -*-
import logging
from .source_base import Origin
__author__ = "imdreamrunner"
__email__ = "imdreamrunner@gmail.com"

ORIGIN_NAME = "TechCrunch"


log = logging.getLogger(__name__)


class TechCrunch(Origin):
    def _list_page_url(self, page_number):
        if page_number == 1:
            return "http://techcrunch.com/"
        else:
            return "http://techcrunch.com/page/" + str(page_number) + "/"


origin = TechCrunch("TechCrunch")
