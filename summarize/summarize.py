# -*- coding: utf8 -*-
import store
import json
from sumy.parsers.html import HtmlParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words


__author__ = "imdreamrunner"
__email__ = "imdreamrunner@gmail.com"

LANGUAGE = "english"
SENTENCES_COUNT = 7


def do():
    rows = store.get_row_by_status(1)

    for row in rows:
        parser = HtmlParser.from_string(row["content_origin"], row["url"], Tokenizer(LANGUAGE))
        stemmer = Stemmer(LANGUAGE)
        summarizer = Summarizer(stemmer)
        summarizer.stop_words = get_stop_words(LANGUAGE)

        sentences = list()

        for sentence in summarizer(parser.document, SENTENCES_COUNT):
            sentences.append(str(sentence))

        summary = "\n".join(sentences)

        store.update_row(row["id"], {"summary_origin": summary, "status": 2})
