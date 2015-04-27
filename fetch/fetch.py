import logging
import store
from util import remote

__author__ = "imdreamrunner"
__email__ = "imdreamrunner@gmail.com"

log = logging.getLogger(__name__)


def fetch():
    rows = store.get_row_by_status(0)
    for row in rows:
        url = row["url"]
        try:
            content = remote.fetch_raw(url)
            if content is not None and len(content) > 0:
                store.update_row(row["id"], {"content_origin": content, "status": 1})
            else:
                raise Exception("Blank content in response.")
        except Exception as e:
            log.warn("Unable to fetch: " + str(e))
            store.update_row(row["id"], {"status": 11})