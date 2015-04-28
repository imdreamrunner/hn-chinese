import shutil
import os
import logging
import requests
import util.common

__author__ = "imdreamrunner"
__email__ = "imdreamrunner@gmail.com"

log = logging.getLogger(__name__)

STORE_BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../images"))


def fetch_raw(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/39.0.2171.95 Safari/537.36'
    }
    r = requests.get(url, headers=headers)
    log.info("Response header: " + r.headers['content-type'])
    if r.status_code == 200 and r.headers['content-type'][:5] == 'text/':
        return r.text
    else:
        return None


def fetch_image(url):
    if not os.path.exists(STORE_BASE_PATH):
        os.mkdir(STORE_BASE_PATH)
    r = requests.get(url, stream=True)
    file_name = util.common.get_file_name(url)
    if r.status_code == 200:
        with open(STORE_BASE_PATH + "/" + file_name, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
    return file_name

