from sys import argv
import src.utils

# TODO do tests

if __name__ == "__main__":
    opts, url = src.utils.parse_arguments(argv)

    src.utils.execute(opts, url)
