# -*- coding: utf8 -*-
"""
Status:
0: URL fetched
1: Content fetched
2: Summary generated
3: Translation finished
4. Keywords generated
11: Failed to fetch content
12: Failed to generate summary
13: Failed to translate
14: Failed to generate keywords
"""
import logging
from . import _mysql

__author__ = "imdreamrunner"
__email__ = "imdreamrunner@gmail.com"


log = logging.getLogger(__name__)


def _execute(sql, arguments=None):
    cursor = _mysql.get_cursor()
    try:
        cursor.execute(sql, arguments)
        log.info("SQL executed: " + str(cursor._last_executed))
    except:
        log.info("SQL executed fails: " + str(cursor._last_executed))
        raise
    _mysql.commit()
    return cursor.fetchall()


def get_row_by_id(row_id):
    rows = _execute("SELECT * FROM `article` WHERE `id` = %s", (row_id,))
    if len(rows) > 0:
        return rows[0]
    else:
        return None


def get_row_by_status(status):
    rows = _execute("SELECT * FROM `article` WHERE `status` = %s ORDER BY `create_time` DESC", (status,))
    return [_parse_row(row) for row in rows]


def save_new_url(row_id, url, title, score, create_time):
    existing = get_row_by_id(row_id)
    if existing is None:
        _execute("INSERT INTO `article` (`id`, `url`, `title_origin`, `score`, `create_time`) "
                 "VALUES (%s, %s, %s, %s, %s)",
                 (row_id, url, title, score, create_time))
        return True
    else:
        return False


def _parse_row(row):
    return {
        "id": row[0],
        "title_origin": row[1].decode("utf-8"),
        "content_origin": row[2].decode("utf-8"),
        "summary_origin": row[3].decode("utf-8"),
        "title_translated": row[4].decode("utf-8"),
        "content_translated": row[5].decode("utf-8"),
        "summary_translated": row[6].decode("utf-8"),
        "image": row[7].decode("utf-8"),
        "tags": row[8].decode("utf-8"),
        "url": row[9],
        "score": row[10],
        "status": row[11],
        "create_time": row[12]
    }


def update_row(row_id, updates):
    sql_set_list = list()
    new_value_list = list()
    for new_key, new_value in updates.iteritems():
        sql_set_list.append("`" + new_key + "` = %s")
        new_value_list.append(new_value)
    sql_query = "UPDATE `article` SET " + ", ".join(sql_set_list)
    sql_query += " WHERE `id` = %s"
    _execute(sql_query, tuple(new_value_list + [row_id]))
