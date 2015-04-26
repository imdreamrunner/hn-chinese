import sys
import logging
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
    if command == "fetch":
        log.debug("Command: fetch")
        fetch.fetch_all()
        summarize.summarize()
        translate.translate()
        tag.tag()
    elif command == "generate":
        log.debug("Command: generate")
        generate.generate()
    else:
        print("Unknown command: " + command)
    log.info("Program exits.")
