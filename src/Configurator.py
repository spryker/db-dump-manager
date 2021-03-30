import yaml


class Configurator:
    def __init__(self):
        self.app_config = yaml.safe_load(open('config.yaml'))
        self.clean_config = yaml.safe_load(open('dump-clean-config.yaml'))

    def get_config(self):
        return self.app_config

    def get_pgsql_config(self):
        return self.app_config.get('pgsql')

    def get_mariadb_config(self):
        return self.app_config.get('mariadb')

    def get_dump_directory(self):
        return self.app_config.get('dump_directory_path')

    def get_clean_config(self):
        return self.clean_config.get('clean')

    def get_replace_config(self):
        return self.clean_config.get('replace')
