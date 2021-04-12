import logging
import os
import time
import subprocess

from src.Configurator.Configurator import Configurator


class DumpUploader:
    config: Configurator

    def __init__(self, config):
        self.config = config
        # todo:refactoring
        self.logger = logging.getLogger('uploader')
        handler = logging.FileHandler('logs/upload_error.log')
        handler.setLevel(logging.ERROR)
        self.logger.addHandler(handler)

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

        # os.system(command)
        result = subprocess.run(command, shell=True, capture_output=True)

        if result.stderr:
            error_msg = result.stderr.decode('utf-8')
            print(error_msg)
            self.logger.critical("File: {} - {}".format(file_path, error_msg))

        time.sleep(2)
