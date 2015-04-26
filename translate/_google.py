# -*- coding: utf8 -*-
import time
import logging
from apiclient.discovery import build

__author__ = "imdreamrunner"
__email__ = "imdreamrunner@gmail.com"


log = logging.getLogger(__name__)


def translate_article(title, content, summary):
    retry = 0
    try:
        return _translate_article(title, content, summary)
    except Exception as ex:
        print(ex)
        retry += 1
        if retry > 3:
            raise ex
        log.info("Translation fails, retry in 3 seconds...")
        time.sleep(3)


def _translate_article(title, content, summary):
    service = build('translate', 'v2', developerKey="")
    result = service.translations().list(target='zh-CN', source='en', q=[title, content, summary]).execute()
    translated = result["translations"][0]["translatedText"]
    return result["translations"][0]["translatedText"], result["translations"][1]["translatedText"], \
           result["translations"][2]["translatedText"]