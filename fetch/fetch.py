from . import source_techcrunch

__author__ = "imdreamrunner"
__email__ = "imdreamrunner@gmail.com"

sources = [source_techcrunch]


def fetch_all():
    for source in sources:
        source.origin.fetch(30)


if __name__ == "__main__":
    fetch_all()