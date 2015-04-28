import sys
import logging
import hn
import fetch
import summarize
import translate
import tag
import generate

__author__ = "imdreamrunner"
__email__ = "imdreamrunner@gmail.com"


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


if __name__ == "__main__":
    print("Welcome to Reader")
    args = sys.argv
    if len(args) != 2:
        print("Usage: python reader.py <fetch|generate>")
        exit(1)
    command = args[1]
    actions = list()
    if command == "crawl":
        log.debug("Command: crawl")
        actions = [hn, fetch, summarize, translate, tag]
    elif command == "hn":
        log.debug("Command: hn")
        actions = [hn]
    elif command == "fetch":
        log.debug("Command: fetch")
        actions = [fetch]
    elif command == "summarize":
        log.debug("Command: summarize")
        actions = [summarize]
    elif command == "translate":
        log.debug("Command: translate")
        actions = [translate]
    elif command == "tag":
        log.debug("Command: tag")
        actions = [tag]
    elif command == "generate":
        log.debug("Command: generate")
        actions = [generate]
    else:
        print("Unknown command: " + command)
    for action in actions:
        action.do()
    log.info("Program exits.")
