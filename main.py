import os
import sys
from os import listdir
from pathlib import Path

from src.Configurator import Configurator
from src.DumpFixer import DumpFixer
from src.DumpUploader import DumpUploader
from src.PoolCreator import PoolCreator
from src.TableReader import TableReader
from src.Timer import Timer


def run_pg_dump_process(config, table_name):
    # todo: config
    dump_directory_path = 'dump/origin'
    command_template = "pg_dump -h localhost -p 15432 -d avag -U avag " \
                       "--data-only " \
                       "--no-owner " \
                       "--no-acl " \
                       "--attribute-inserts " \
                       "--disable-dollar-quoting " \
                       "--no-tablespaces " \
                       "--table {} -f {}"

    file_name_template = "{}/{}.sql"

    file_name = file_name_template.format(dump_directory_path, table_name)

    timer = Timer()
    os.system(command_template.format(table_name, file_name))
    timer.stop()

    return "Table: {} was dumped - {} seconds.".format(table_name, timer.get_time_in_seconds())


def run_cleanup_process(config, file_path):
    timer = Timer()
    # todo: fix file_path
    DumpFixer(config).run(file_path)
    timer.stop()

    return "File: {} was cleaned - {} seconds.".format(Path(file_path).name, timer.get_time_in_seconds())


def run_upload_process(config, file_path):
    timer = Timer()
    DumpUploader(config).run(file_path)
    timer.stop()

    return "File {} was uploaded - {} seconds.".format(file_path, timer.get_time_in_seconds())


def start_dumping_pool(config):
    os.environ["PGPASSWORD"] = config.get_pgsql_config().get('password')

    timer = Timer()

    table_reader = TableReader(**config.get_pgsql_config())
    table_name_list: list[str] = table_reader.get_table_name_list()
    run_process_iterator = PoolCreator(config).create_pool_iterator(run_pg_dump_process, table_name_list)

    iterator = 1
    max_table_len = len(table_name_list)
    for x in run_process_iterator:
        print("[{}/{}] {}".format(iterator, max_table_len, x))
        iterator += 1

    timer.stop()
    print("Dumping process ran in about {} seconds.".format(timer.get_time_in_seconds()), flush=True)

    os.environ["PGPASSWORD"] = ''


def starting_cleanup_pool(config):
    timer = Timer()

    # todo: config
    dump_origin_path = 'dump/origin'
    file_name_list = ['{}/{}'.format(dump_origin_path, f) for f in listdir(dump_origin_path)]

    run_process_iterator = PoolCreator(config).create_pool_iterator(run_cleanup_process, file_name_list)

    iterator = 1
    max_table_len = len(file_name_list)
    for x in run_process_iterator:
        print("[{}/{}] {}".format(iterator, max_table_len, x))
        iterator += 1

    timer.stop()
    print("Cleanup process ran in about {} seconds.".format(timer.get_time_in_seconds()), flush=True)


def starting_upload_pool(config):
    timer = Timer()

    dump_clean_path = 'dump/clean'
    file_name_list = ['{}/{}'.format(dump_clean_path, f) for f in listdir(dump_clean_path)]
    DumpUploader(config).run('sql-scripts/start.sql')

    run_process_iterator = PoolCreator(config).create_pool_iterator(run_upload_process, file_name_list)

    iterator = 1
    max_table_len = len(file_name_list)
    for x in run_process_iterator:
        print("[{}/{}] {}".format(iterator, max_table_len, x))
        iterator += 1

    DumpUploader(config).run('sql-scripts/finish.sql')
    timer.stop()
    print("Upload process ran in about {} seconds.".format(timer.get_time_in_seconds()), flush=True)


if __name__ == "__main__":
    config = Configurator()
    timer = Timer()

    args = sys.argv[1:]

    # todo: refactoring
    if len(args) == 0:
        start_dumping_pool(config)
        starting_cleanup_pool(config)
        starting_upload_pool(config)
    else:
        for arg in args:
            if arg == 'dump':
                start_dumping_pool(config)

            if arg == 'clean':
                starting_cleanup_pool(config)

            if arg == 'upload':
                starting_upload_pool(config)

    timer.stop()
    print("Full process ran in about {} seconds.".format(timer.get_time_in_seconds()), flush=True)
