import logging
import json
import store
import multiprocessing
from multiprocessing.pool import ThreadPool
from util import remote

__author__ = "imdreamrunner"
__email__ = "imdreamrunner@gmail.com"

log = logging.getLogger(__name__)


SOURCE_LIST = [
    "https://hacker-news.firebaseio.com/v0/topstories.json",
    # "https://hacker-news.firebaseio.com/v0/newstories.json"
]

MIN_SCORE = 50

_number_processed = 0
_number_total = 0


def do():
    global _number_total, _number_processed
    for source in SOURCE_LIST:
        raw = remote.fetch_raw(source)
        ids = json.loads(raw)
        thread_number = multiprocessing.cpu_count()
        log.info("Create thread pool size of " + str(thread_number) + ".")
        thread_pool = ThreadPool(thread_number)
        _number_total = len(ids)
        _number_processed = 0
        for item_id in ids:
            thread_pool.apply_async(fetch_single, [item_id])
        thread_pool.close()
        thread_pool.join()


def fetch_single(item_id):
    global _number_total, _number_processed
    _number_processed += 1
    log_prefix = "[ITEM " + str(item_id) + "]"
    log.info(log_prefix + "Fetch started. (" + str(_number_processed) + " of " + str(_number_total) + ")")
    url = "https://hacker-news.firebaseio.com/v0/item/" + str(item_id) + ".json"
    raw = remote.fetch_raw(url)
    story = json.loads(raw)
    if check_condition(story):
        if store.save_new_url(story["id"], story["url"], story["title"], story["score"], story["time"]):
            log.info(log_prefix + "Story saved.")
        else:
            log.info(log_prefix + "Story has been stored.")
    else:
        log.info(log_prefix + "Story is skipped because it does not meet the minimal requirement.")
        log.debug(raw)


def check_condition(story):
    return "score" in story and story["score"] > MIN_SCORE and\
           story["type"] == "story" and "parent" not in story and\
           story["title"][:7] != "Ask HN:"
