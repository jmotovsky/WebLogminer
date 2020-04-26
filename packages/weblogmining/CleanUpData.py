from typing import Set, Dict
from os import path as path
from .filereader import FileReaderParallel
from .datatransformation import BaseCleanUpSequence, PreRobotsIdentitySequence, BlankIdentitySequence
from .PreProcessRobots import PreProcessRobots


def _line_format(line: Dict[str, str]) -> str:
    return '\t'.join(line.values())


class CleanUpData:
    def __init__(self, input_file_name: str, output_file_name: str, temp_file_name: str = 'temp.log'):
        self.__input_file_name = input_file_name
        self.__output_file_name = output_file_name
        self.__temp_file_name = path.dirname(path.normpath(output_file_name)) + '/' + temp_file_name

    def run(self, chunk_robots_size: int = 50):
        pre_robots_clean_data = self.__base_clean(chunk_robots_size)
        robots_clean_data = self.__identify_robots(pre_robots_clean_data)
        self.__safe_cleaned_data(robots_clean_data)

    def __base_clean(self, chunk_robots_size: int) -> Dict[str, str]:
        total_search_robots = set()
        pre_process_robots = PreProcessRobots(self.__temp_file_name, chunk_robots_size)
        pre_robots_identity_sequence = PreRobotsIdentitySequence()

        with open(self.__temp_file_name, 'w') as f:
            for job_order, items in FileReaderParallel(self.__input_file_name).manage_work(BaseCleanUpSequence()):
                for item in items:
                    line = _line_format(item)
                    f.write(line + '\n')
                    robots = pre_robots_identity_sequence.process_data(line)
                    if robots and robots['IP'] not in total_search_robots:
                        ip = robots['IP']
                        agent = robots['Agent']
                        total_search_robots.add(ip)
                        pre_process_robots.add([ip, agent])

        pre_process_robots.run_jobs()

        return pre_process_robots.get_jobs()

    def __identify_robots(self, pre_robots_clean_data: Dict[str, str]) -> Set:
        robots_clean_data = set()
        for ip, jobs in pre_robots_clean_data.items():
            i = 0
            for job_order, line_states in jobs:
                for line_state in line_states:
                    if line_state and i not in robots_clean_data:
                        robots_clean_data.add(i)

                    i += 1

        return robots_clean_data

    def __safe_cleaned_data(self, robots_clean_data: Set) -> None:
        with open(self.__output_file_name, 'w') as f:
            i = 0
            for job_order, items in FileReaderParallel(self.__temp_file_name).manage_work(BlankIdentitySequence()):
                for item in items:
                    if i not in robots_clean_data:
                        f.write(item + '\n')

                    i += 1
