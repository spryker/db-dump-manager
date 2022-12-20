import os
from src.Configurator.Configurator import Configurator
from src.Configurator.State.DumpState import DumpState
from src.PoolCreator import PoolCreator
from src.TableReader import TableReader
from src.Timer import Timer
from progress.bar import Bar



def start_dumping_pool(config: Configurator):
    run_process_iterator = None
    iteration_length = 0
    dump_mode = config.get_dump_mode()

    if dump_mode is DumpState.tables:
        table_name_list = get_table_name_list(config)
        run_process_iterator = create_dump_pool_by_tables(config, table_name_list)
        iteration_length = len(table_name_list)

    if dump_mode is DumpState.file:
        run_process_iterator = create_dump_pool_by_file(config)
        iteration_length = 1

    timer = Timer()

    iterator = 1

    bar = Bar('Processing', max=iteration_length)
    for x in run_process_iterator:
        if config.get_verbose():
            print("[{}/{}] {}".format(iterator, iteration_length, x))
            iterator += 1
        else:
            bar.next()

    bar.finish()
    timer.stop()

    print("Dumping process run in about {} seconds.".format(timer.get_time_in_seconds()), flush=True)


def get_table_name_list(config):
    table_reader = TableReader(**config.get_pgsql_config())
    return table_reader.get_table_name_list()


def create_dump_pool_by_tables(config, table_name_list):
    return PoolCreator(config).create_pool_iterator(run_pg_dump_process_by_tables, table_name_list)


def create_dump_pool_by_file(config):
    return PoolCreator(config).create_pool_iterator(run_pg_dump_process_by_file, (None,))


def run_pg_dump_process_by_file(config: Configurator, pool_arg):
    dump_directory_path = './dump/origin'
    command_template = "PGPASSWORD={} pg_dump -h {} -p {} -d {} -U {} " \
                       "--data-only " \
                       "--no-owner " \
                       "--no-acl " \
                       "--attribute-inserts " \
                       "--disable-dollar-quoting " \
                       "--no-tablespaces " \
                       "--rows-per-insert={} " \
                       "-f {}"

    file_name_template = "{}/{}.sql"
    file_name = file_name_template.format(dump_directory_path, 'full-dump')

    command = command_template.format(
        config.get_pgsql_config().get('password'),
        config.get_pgsql_config().get('host'),
        config.get_pgsql_config().get('port'),
        config.get_pgsql_config().get('dbname'),
        config.get_pgsql_config().get('user'),
        config.get_rows_per_insert(),
        file_name
    )

    timer = Timer()
    os.system(command)
    timer.stop()

    return "Full dump was dumped - {} seconds.".format(timer.get_time_in_seconds())


def run_pg_dump_process_by_tables(config, table_name):
    dump_directory_path = './dump/origin'
    command_template = "PGPASSWORD={} pg_dump -h {} -p {} -d {} -U {} " \
                       "--data-only " \
                       "--no-owner " \
                       "--no-acl " \
                       "--attribute-inserts " \
                       "--disable-dollar-quoting " \
                       "--no-tablespaces " \
                       "--rows-per-insert={} " \
                       "--table {} -f {}"

    file_name_template = "{}/{}.sql"
    file_name = file_name_template.format(dump_directory_path, table_name)

    command = command_template.format(
            config.get_pgsql_config().get('password'),
            config.get_pgsql_config().get('host'),
            config.get_pgsql_config().get('port'),
            config.get_pgsql_config().get('dbname'),
            config.get_pgsql_config().get('user'),
            config.get_rows_per_insert(),
            table_name,
            file_name
        )

    timer = Timer()
    os.system(command)
    timer.stop()

    return "Table: {} was dumped - {} seconds.".format(table_name, timer.get_time_in_seconds())
