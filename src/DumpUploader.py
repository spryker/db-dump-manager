import os
import time

from src.Configurator.Configurator import Configurator


class DumpUploader:
    config: Configurator

    def __init__(self, config):
        self.config = config

    def run(self, file_path):
        command_template = 'MYSQL_PWD={} mysql --database={} --user={} --host={} --port={} < {}'
        command = command_template.format(
            self.config.get_mariadb_config().get('password'),
            self.config.get_mariadb_config().get('dbname'),
            self.config.get_mariadb_config().get('user'),
            self.config.get_mariadb_config().get('host'),
            self.config.get_mariadb_config().get('port'),
            file_path
        )

        os.system(command)
        time.sleep(2)
