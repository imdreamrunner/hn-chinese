import logging
import time
import goslate

__author__ = "imdreamrunner"
__email__ = "imdreamrunner@gmail.com"


log = logging.getLogger(__name__)
gs = goslate.Goslate()


def _translate_single(origin):
    return gs.translate(origin, 'zh-CN')



def translate_article(title, content, summary):
    retry = 0
    try:
        return _translate_single(title), _translate_single(content), _translate_single(summary)
    except Exception as ex:
        print(ex)
        retry += 1
        if retry > 3:
            raise ex
        log.info("Translation fails, retry in 3 seconds...")
        time.sleep(3)