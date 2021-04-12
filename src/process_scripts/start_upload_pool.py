import logging
from os import listdir
from progress.bar import Bar
from src.Configurator.Configurator import Configurator
from src.DumpUploader import DumpUploader
from src.PoolCreator import PoolCreator
from src.Timer import Timer


def run_start_scripts(config: Configurator):
    if config.get_global_script_config() is True:
        DumpUploader(config).run('./sql-scripts/start/global.sql')

    if config.get_session_script_config() is True:
        DumpUploader(config).run('./sql-scripts/start/session.sql')


def run_finish_scripts(config: Configurator):
    if config.get_global_script_config() is True:
        DumpUploader(config).run('./sql-scripts/finish/global.sql')

    if config.get_session_script_config() is True:
        DumpUploader(config).run('./sql-scripts/finish/session.sql')


def start_upload_pool(config: Configurator):
    timer = Timer()
    # todo: refactoring
    logger = logging.getLogger('uploader_script')
    handler = logging.FileHandler('logs/upload.log')
    handler.setLevel(logging.WARNING)
    logger.addHandler(handler)

    # todo: config
    dump_clean_path = 'dump/clean'
    file_name_list = ['{}/{}'.format(dump_clean_path, f) for f in listdir(dump_clean_path)]
    run_start_scripts(config)

    run_process_iterator = PoolCreator(config).create_pool_iterator(run_upload_process, file_name_list)

    iterator = 1
    max_table_len = len(file_name_list)
    bar = Bar('Processing', max=max_table_len)
    for x in run_process_iterator:
        if config.get_verbose():
            msg = "[{}/{}] {}".format(iterator, max_table_len, x)
            logger.warning(msg)
            print(msg)

            iterator += 1
        else:
            bar.next()

    run_finish_scripts(config)
    timer.stop()

    finish_msg = "Upload process ran in about {} seconds.".format(timer.get_time_in_seconds())
    logger.warning(finish_msg)
    print(finish_msg, flush=True)


def run_upload_process(config, file_path):
    timer = Timer()
    # todo: exception
    DumpUploader(config).run(file_path)
    timer.stop()

    return "File {} was uploaded - {} seconds.".format(file_path, timer.get_time_in_seconds())
