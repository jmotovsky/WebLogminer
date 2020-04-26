import os.path
from typing import Iterable, IO, Tuple


class Chunker(object):
    @classmethod
    def chunkify(cls, file_name: str, size: int = 1024 * 1024) -> Tuple[int, list]:
        file_end = os.path.getsize(file_name)
        with open(file_name, 'rb') as file:
            chunk_end = file.tell()
            while True:
                chunk_start = chunk_end
                file.seek(size, 1)
                cls._EOC(file)
                chunk_end = file.tell()
                yield chunk_start, chunk_end - chunk_start
                if chunk_end >= file_end:
                    break

    @staticmethod
    def _EOC(file: IO) -> None:
        file.readline()

    @staticmethod
    def read(file_name: str, chunk: list) -> str:
        with open(file_name, 'r') as file:
            file.seek(chunk[0])
            return file.read(chunk[1])

    @staticmethod
    def parse(chunk: str) -> Iterable[str]:
        for line in chunk.splitlines():
            yield line
