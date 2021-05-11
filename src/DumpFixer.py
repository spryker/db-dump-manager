from pathlib import Path
from re import search


class DumpFixer:
    # todo: config
    __dump_clean_directory_path__ = 'dump/clean'

    def __init__(self, config):
        self.config = config

    def run(self, file_path):
        file_name = Path(file_path).name
        dump_clean_file_path = '{}/{}'.format(self.__dump_clean_directory_path__, file_name)

        dump_origin = open(file_path, "rt")
        dump_clean = open(dump_clean_file_path, "w+")

        dump_clean.write('begin;\n')

        for line in dump_origin:
            cleaned_line = self.__clean_up__(line)
            cleaned_line = self.__replace__(cleaned_line)

            if not cleaned_line.strip():
                continue

            cleaned_line = self.__json_values_unicode_build__(cleaned_line)
            dump_clean.write(cleaned_line)

        dump_clean.write('commit;\n')
        dump_origin.close()
        dump_clean.close()

    def __clean_up__(self, line):
        clean_line = line
        for clean_pattern in self.config.get_clean_config():
            if search(clean_pattern, clean_line):
                clean_line = ''

        return clean_line

    def __replace__(self, line):
        if not line:
            return line

        replace_config = self.config.get_replace_config()

        for replace_list in replace_config:
            line = line.replace(replace_list[0], replace_list[1])

        return line

    def __json_values_unicode_build__(self, cleaned_line):
        # todo: refactoring
        values_start_index = cleaned_line.find('VALUES (')
        if values_start_index == -1:
            return cleaned_line

        values_string = cleaned_line[values_start_index:]

        json_index_start = values_string.find('\'{')
        if json_index_start == -1:
            return cleaned_line

        json_index_stop = values_string.rfind('}\'') + 2
        json_str = values_string[json_index_start:json_index_stop]

        json_str = json_str.lstrip('\'')
        json_str = json_str.rstrip('\'')
        json_str = json_str.replace('\\', '\\\\')

        json_str = '\'{}\''.format(json_str)
        full_string = values_string[:json_index_start] + json_str + values_string[json_index_stop:]

        return cleaned_line[:values_start_index] + full_string
