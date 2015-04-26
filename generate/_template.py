# -*- coding: utf8 -*-
import os
import jinja2
import logging
from . import url

__author__ = "imdreamrunner"
__email__ = "imdreamrunner@gmail.com"


log = logging.getLogger(__name__)

TEMPLATE_BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../templates"))

templateLoader = jinja2.FileSystemLoader(TEMPLATE_BASE_PATH)
templateEnv = jinja2.Environment(loader=templateLoader)
templateEnv.globals["url"] = url


def get_template(name):
    log.info("Load template " + TEMPLATE_BASE_PATH + "/" + name + ".jinja2")
    return templateEnv.get_template(name + ".jinja2")