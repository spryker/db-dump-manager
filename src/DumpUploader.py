import os

from src.Configurator import Configurator


class DumpUploader:
    config: Configurator

    def __init__(self, config):
        self.config = config

    def run(self, file_path):
        command_template = 'mysql --database={} --user={} --host={} --port={} < {} --password={}'
        command = command_template.format(
            self.config.get_mariadb_config().get('dbname'),
            self.config.get_mariadb_config().get('user'),
            self.config.get_mariadb_config().get('host'),
            self.config.get_mariadb_config().get('port'),
            file_path,
            self.config.get_mariadb_config().get('password'),
        )

        os.system(command + ' > maria_output.log 2>&1')
