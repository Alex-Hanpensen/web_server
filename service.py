import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


class WebServer:

    def __init__(self, file_name: str, cmd1: str, value1: str | bool, value2: str | bool | None = None,
                 cmd2: str | None = None):
        self.file_name = fr'{DATA_DIR}\{file_name}'
        self.cmd1 = cmd1
        self.value1 = value1
        self.cmd2 = cmd2
        self.value2 = value2

    def controller(self, cmd: str, value, filtered_data=None):
        """
        the excitement of the team by the selected value
        :param cmd: command for filtering or sorting (str)
        :param value: value (str | int | bool | None)
        :param filtered_data: data from the log
        :return: filter | gener obj
        """
        if not filtered_data:
            filtered_data = self.iter_file(self.read_file())

        if cmd == 'filter':
            return filter(lambda x: value in x, filtered_data)
        elif cmd.lower() == 'map':
            return map(lambda x: re.split(r'\"| - - ', x, 2)[int(value)], filtered_data)
        elif cmd == 'unique':
            return set(filtered_data)
        elif cmd == 'sort':
            return sorted(filtered_data, reverse=value)
        elif cmd == 'limit':
            return (next(filtered_data) for _ in range(int(value)))

    def get_start(self):
        """
        starting the handler
        :return: filter | gener obj
        """
        result = self.controller(self.cmd1.lower(), self.value1)
        if self.cmd2 is None:
            return result
        else:
            return self.controller(self.cmd2.lower(), self.value2, filtered_data=result)

    def read_file(self):
        try:
            file = open(self.file_name)
            return file
        except FileNotFoundError:
            return 400, 'File Not Found Error: No such file or directory'

    @staticmethod
    def iter_file(file):
        while True:
            try:
                line = next(file)
                yield line
            except StopIteration:
                break
