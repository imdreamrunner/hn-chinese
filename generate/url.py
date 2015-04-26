from util import common

__author__ = "imdreamrunner"
__email__ = "imdreamrunner@gmail.com"

EXTENSION = ".html"


def index(page):
    if page == 1:
        return "index" + EXTENSION
    else:
        return "index_" + str(page) + EXTENSION


def article(page):
    return "article_" + str(page) + EXTENSION


def tag(name, page):
    if page == 1:
        return "tag_" + name + EXTENSION
    else:
        return "tag_" + name + "_" + str(page) + EXTENSION


def image(origin_img):
    return "images/" + common.get_file_name(origin_img)