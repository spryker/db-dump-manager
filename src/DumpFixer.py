from pathlib import Path
from re import search


class DumpFixer:

    def __init__(self, config):
        self.config = config

    def run(self, file_path):
        file_name = Path(file_path).name
        dump_clean_file_path = '{}/{}'.format(self.config.get_clean_directory_path(), file_name)

        dump_origin = open(file_path, "rt")
        dump_clean = open(dump_clean_file_path, "w+")

        dump_clean.write('begin;\n')

        for line in dump_origin:
            cleaned_line = self.__clean_up__(line)
            cleaned_line = self.__replace__(cleaned_line)

            if not cleaned_line.strip():
                continue

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
