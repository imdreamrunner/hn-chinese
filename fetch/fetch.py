from . import source_techcrunch, source_thevergetech

__author__ = "imdreamrunner"
__email__ = "imdreamrunner@gmail.com"

sources = [source_thevergetech]


def fetch_all():
    for source in sources:
        source.origin.fetch(5)


if __name__ == "__main__":
    fetch_all()