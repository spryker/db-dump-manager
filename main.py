import sys

from src.Configurator.Configurator import Configurator
from src.Timer import Timer
from src.process_scripts.start_cleanup_pool import start_cleanup_pool
from src.process_scripts.start_dumping_pool import start_dumping_pool
from src.process_scripts.start_upload_pool import start_upload_pool


def start_full_process(config):
    timer = Timer()

    start_dumping_pool(config)
    start_cleanup_pool(config)
    start_upload_pool(config)

    timer.stop()
    print("Full process run in about {} seconds.".format(timer.get_time_in_seconds()), flush=True)


def start_partial_process(args, config):
    for arg in args:
        if arg == 'dump':
            start_dumping_pool(config)

        if arg == 'clean':
            start_cleanup_pool(config)

        if arg == 'upload':
            start_upload_pool(config)


def run(args):
    config = Configurator(verbose='-v' in args)
    timer = Timer()

    if len(args) == 0:
        start_full_process(config)
    else:
        start_partial_process(args, config)

    timer.stop()
    print("Full process run in about {} seconds.".format(timer.get_time_in_seconds()), flush=True)


if __name__ == "__main__":
    run(sys.argv[1:])
