# -*- coding: utf8 -*-
import store
# from ._google import translate_article
from ._goslate import translate_article

__author__ = "imdreamrunner"
__email__ = "imdreamrunner@gmail.com"


def translate():
    rows = store.get_row_by_status(2)
    for row in rows:
        try:
            title_translated, content_translated, summary_translated = translate_article(
                row["title_origin"],
                row["content_origin"],
                row["summary_origin"]
            )
            store.update_row(row["id"], {
                "title_translated": title_translated,
                "content_translated": content_translated,
                "summary_translated": summary_translated,
                "status": 3
            })
        except:
            store.update_row(row["id"], {
                "status": 13
            })