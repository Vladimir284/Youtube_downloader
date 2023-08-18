from src import utils

# TODO do tests

if __name__ == "__main__":
    utils.print_debug_important("=", "DEBUG  INIT")

    url, opts = utils.parse_arguments(utils.sys.argv)

    utils.execute(url, opts)

    print("Videos installed")
    utils.end("=", "DEBUG  DONE")
