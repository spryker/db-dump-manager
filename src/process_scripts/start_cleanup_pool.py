from os import listdir
from pathlib import Path
from re import search
from progress.bar import Bar
from src.Configurator.Configurator import Configurator
from src.Configurator.State.CleanState import CleanState
from src.DumpFixer import DumpFixer
from src.PoolCreator import PoolCreator
from src.Timer import Timer


def start_cleanup_pool(config: Configurator):
    timer = Timer()

    # todo: config
    dump_origin_path = './dump/origin'
    file_name_list = ['{}/{}'.format(dump_origin_path, f) for f in listdir(dump_origin_path) if f != '.gitkeep']
    iteration_length = len(file_name_list)

    clean_mode = config.get_clean_mode()

    if clean_mode is CleanState.tables:
        run_process_iterator = PoolCreator(config).create_pool_iterator(run_cleanup_process, file_name_list)
        iterator = 1

        bar = Bar('Processing', max=iteration_length)
        for x in run_process_iterator:
            if config.get_verbose():
                print("[{}/{}] {}".format(iterator, iteration_length, x))
                iterator += 1
            else:
                bar.next()

        timer.stop()
        print("Cleanup process run in about {} seconds.".format(timer.get_time_in_seconds()), flush=True)

    if clean_mode is CleanState.file:
        dump_clean_file_path = '{}/{}'.format('dump/clean', 'full-dump.sql')
        dump_clean = open(dump_clean_file_path, "w+")
        dump_clean.write('begin;\n')

        bar = Bar('Processing', max=iteration_length)
        for file_path in file_name_list:
            dump_origin = open(file_path, "rt")
            for line in dump_origin:
                cleaned_line = __clean_up__(line, config)
                cleaned_line = __replace__(cleaned_line, config)

                dump_clean.write(cleaned_line)

            dump_origin.close()
            bar.next()

        dump_clean.write('commit;\n')
        dump_clean.close()


def __clean_up__(line, config):
    clean_line = line
    for clean_pattern in config.get_clean_config():
        if search(clean_pattern, clean_line):
            clean_line = ''

    return clean_line


def __replace__(line, config):
    if not line:
        return line

    replace_config = config.get_replace_config()

    for replace_list in replace_config:
        line = line.replace(replace_list[0], replace_list[1])

    return line


def run_cleanup_process(config, file_path):
    timer = Timer()
    # todo: fix file_path
    DumpFixer(config).run(file_path)
    timer.stop()

    return "File: {} was cleaned - {} seconds.".format(Path(file_path).name, timer.get_time_in_seconds())
