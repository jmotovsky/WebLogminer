from abc import abstractmethod
from typing import List
from ..filereader.Sequence import BaseSequence
from .process import process_base_data, process_robots, process_pre_robots

__all__ = ['BaseCleanUpSequence', 'PreRobotsIdentitySequence', 'RobotsIdentitySequence', 'BlankIdentitySequence']


class BlankIdentitySequence(BaseSequence):
    def worker(self, data: List[str]) -> list:
        return data


class DataTransformation(BaseSequence):
    def worker(self, data: List[str]) -> list:
        output_data = []
        for line in data:
            cleaned_data = self.process_data(line)
            output_data += [cleaned_data] if cleaned_data is not None else []
        return output_data

    @abstractmethod
    def process_data(self, line: str):
        pass


class BaseCleanUpSequence(DataTransformation):
    def process_data(self, line: str):
        return process_base_data(line)


class PreRobotsIdentitySequence(DataTransformation):
    def process_data(self, line: str):
        return process_pre_robots(line)


class RobotsIdentitySequence(DataTransformation):
    def __init__(self, robots: list):
        self.__search_ip = [i[0] for i in robots]
        self.__search_agent = [i[1] for i in robots]

    def process_data(self, line: str):
        return process_robots(line, self.__search_ip, self.__search_agent)
