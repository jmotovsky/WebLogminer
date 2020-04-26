import math
from abc import ABC, abstractmethod
from .SQLiteDatabase import SQLiteDatabase
from .sql_structure import get_average_event_intensity


class LengthHeuristic(ABC):
    @abstractmethod
    def max_allowed_time(self) -> float:
        pass

    @abstractmethod
    def session_type(self) -> str:
        pass


class RLengthHeuristic(LengthHeuristic):
    def __init__(self, navigation_ratio: float):
        self.__navigation_ratio = navigation_ratio
        self.__average_event_intensity = SQLiteDatabase.query((get_average_event_intensity())).fetchone()[0]

    def max_allowed_time(self) -> float:
        return - math.log(1 - self.__navigation_ratio) / self.__average_event_intensity

    def session_type(self) -> str:
        return 'session_id_rlength'


class STTQLengthHeuristic(LengthHeuristic):
    def __init__(self, stt_q: float):
        self.__stt_q = stt_q

    def max_allowed_time(self) -> float:
        return self.__stt_q

    def session_type(self) -> str:
        return 'session_id_sttq'


class SLengthLengthHeuristic(LengthHeuristic):
    def __init__(self, estimate: float):
        self.__estimate = estimate

    def max_allowed_time(self) -> float:
        return self.__estimate

    def session_type(self) -> str:
        return 'session_id_slength'
