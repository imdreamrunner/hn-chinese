import shutil
import os
import logging
import requests
import util.common

__author__ = "imdreamrunner"
__email__ = "imdreamrunner@gmail.com"

log = logging.getLogger(__name__)

STORE_BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../images"))


def fetch_html(url):
    r = requests.get(url)
    if r.status_code == 200:
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

