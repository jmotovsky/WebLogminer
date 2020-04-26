import queue
from typing import Dict
from .filereader import FileReaderParallel
from .datatransformation import RobotsIdentitySequence


class SearchRobots(queue.Queue):
    def get_more(self, amount):
        elements = []
        i = 0
        while i < amount and not self.empty():
            elements.append(self.get())
            i += 1

        return elements


class PreProcessRobots:
    def __init__(self, input_file: str, chunk_size: int):
        self.__input_file = input_file
        self.__chunk_size = chunk_size

        self.__counter = 0
        self.__job_counter = 0

        self.__pre_robots_clean_data = {}
        self.__search_robots = SearchRobots()

    def add(self, data: list) -> None:
        self.__counter += 1
        self.__search_robots.put(data)

        if self.__counter == self.__chunk_size:
            self.__run_job()
            self.__set_default_counter()

    def __run_job(self) -> None:
        data = self.__search_robots.get_more(self.__chunk_size)
        self.__pre_robots_clean_data[self.__job_counter] = FileReaderParallel(self.__input_file).manage_work(RobotsIdentitySequence(data))
        self.__job_counter += 1

    def run_jobs(self) -> None:
        while not self.__search_robots.empty():
            self.__run_job()

        self.__set_default_counter()

    def get_jobs(self) -> Dict:
        if not self.__search_robots.empty():
            self.run_jobs()

        return self.__pre_robots_clean_data

    def __set_default_counter(self) -> None:
        self.__counter = 0
