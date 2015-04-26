import hashlib

__author__ = "imdreamrunner"
__email__ = "imdreamrunner@gmail.com"


def get_file_name(url):
    m = hashlib.md5()
    m.update(url)
    extension = url.split(".")[-1].split("#")[0].split("?")[0].lower()
    return m.hexdigest() + "." + extension