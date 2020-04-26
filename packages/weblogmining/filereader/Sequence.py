from typing import List

from abc import ABC, abstractmethod


class BaseSequence(ABC):
    @abstractmethod
    def worker(self, data: List[str]) -> list:
        pass
