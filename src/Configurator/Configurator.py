import yaml

from src.Configurator.State.CleanState import CleanState
from src.Configurator.State.DumpState import DumpState


class Configurator:
    verbose: bool

    def __init__(self, verbose=False):
        self.verbose = verbose
        self.app_config = yaml.safe_load(open('config.yaml'))
        self.clean_config = yaml.safe_load(open('dump-clean-config.yaml'))

    def get_verbose(self):
        return self.verbose

    def get_config(self):
        return self.app_config

    def get_pgsql_config(self):
        return self.app_config.get('pgsql')

    def get_rows_per_insert(self):
        return self.app_config.get('rows_per_insert')

    def get_mariadb_config(self):
        return self.app_config.get('mariadb')

    def get_dump_directory_path(self):
        return self.app_config.get('dump_directory_path')

    def get_clean_directory_path(self):
        return self.app_config.get('clean_directory_path')

    def get_clean_config(self):
        return self.clean_config.get('clean')

    def get_replace_config(self):
        return self.clean_config.get('replace')

    def get_dump_mode(self):
        config_value = self.app_config.get('dump').lower()

        if config_value in DumpState.__members__:
            return DumpState[config_value]

        return DumpState.default

    def get_clean_mode(self):
        config_value = self.app_config.get('clean').lower()

        if self.get_dump_mode() is not DumpState.tables:
            return CleanState.file

        if config_value in CleanState.__members__:
            return CleanState[config_value]

        return CleanState.default

    def get_global_script_config(self):
        return self.app_config.get('scripts').get('global') or False

    def get_session_script_config(self):
        return self.app_config.get('scripts').get('session') or True
