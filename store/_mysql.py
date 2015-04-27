import MySQLdb

__author__ = "imdreamrunner"
__email__ = "imdreamrunner@gmail.com"


_db = None


def get_cursor():
    global _db
    if _db is None:
        _db = MySQLdb.connect("localhost", "hn-chinese", "reader", "reader" )
    return _db.cursor()


def commit():
    if _db is not None:
        _db.commit()
