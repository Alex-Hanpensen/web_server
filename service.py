import os
import re
from typing import Tuple, TextIO, Optional, Generator

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


class WebServer:

    def __init__(self, file_name: str, cmd1: str, value1: str, value2: str,
                 cmd2: str) -> None:
        self.file_name: str = fr'{DATA_DIR}\{file_name}'
        self.cmd1: str = cmd1
        self.value1: str = value1
        self.cmd2: str = cmd2
        self.value2: str = value2

    def controller(self, cmd: str, value: str, filtered_data=None):
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
            revers = True if value == 'asc' else False
            return sorted(filtered_data, reverse=revers)
        elif cmd == 'limit':
            return (next(filtered_data) for _ in range(int(value)))
        elif cmd == 'regex':
            return (data for data in filtered_data if re.search(value, data))

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

    def read_file(self) -> TextIO | tuple[int, str]:
        try:
            file = open(self.file_name)
            return file
        except FileNotFoundError:
            return 400, 'File Not Found Error: No such file or directory'

    @staticmethod
    def iter_file(file) -> Generator:
        while True:
            try:
                line = next(file)
                yield line
            except StopIteration:
                break
