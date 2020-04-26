from os import cpu_count
from enum import Enum
from typing import Type
from .Chunker import Chunker


class ChunkerEnum(Enum):
    Base = 0


class FileReaderParallelConfig(object):
    def __init__(self, chunker: ChunkerEnum = ChunkerEnum.Base, cores: int = cpu_count()):
        self.__chunker = self.__set_chunker(chunker)
        self.__cores = cores

    @property
    def chunker(self) -> Type[Chunker]:
        return self.__chunker

    @property
    def cores(self) -> int:
        return self.__cores

    def __set_chunker(self, chunker: ChunkerEnum) -> Type[Chunker]:
        switcher = {
            ChunkerEnum.Base: Chunker
        }

        return switcher.get(chunker, Chunker)
