# -*- coding: utf8 -*-
import store
import jieba
import jieba.analyse

__author__ = "imdreamrunner"
__email__ = "imdreamrunner@gmail.com"


def do():
    rows = store.get_row_by_status(3)
    for row in rows:
        try:
            keywords = jieba.analyse.extract_tags(row["summary_translated"], topK=7)
            store.update_row(row["id"], {
                "tags": ",".join(keywords),
                "status": 4
            })
        except:
            store.update_row(row["id"], {
                "status": 14
            })

