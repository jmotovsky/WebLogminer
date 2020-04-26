from typing import Optional
from abc import ABC, abstractmethod
from .LengthHeuristic import LengthHeuristic
from .SQLiteDatabase import SQLiteDatabase
from .sql_structure import update_web_mining_session_id


class SessionCounter(ABC):
    def __init__(self, length_heuristic: LengthHeuristic):
        self.__length_heuristic = length_heuristic
        self._reset()

    @property
    def _length_heuristic(self) -> LengthHeuristic:
        return self.__length_heuristic

    def check_user_id(self, new_user_id: str, current_user_id: str) -> bool:
        state = False

        if new_user_id != current_user_id:
            state = True

            if len(self.__group_ids) > 0:
                SQLiteDatabase.query(
                    update_web_mining_session_id(
                        self.__length_heuristic.session_type(), self.__session_id, self.__group_ids
                    )
                )

            self._reset()

        return state

    def check_length(self, length: Optional[int]) -> None:
        if length is None or self._compare_length(length):
            SQLiteDatabase.query(
                update_web_mining_session_id(
                    self.__length_heuristic.session_type(), self.__session_id, self.__group_ids
                )
            )

            self._increase()

    def add_id(self, item: str) -> None:
        self.__group_ids.append(item)

    @abstractmethod
    def _compare_length(self, length: int) -> bool:
        pass

    def _reset(self) -> None:
        self.__session_id = 1
        self.__group_ids = []

    def _increase(self) -> None:
        self.__session_id += 1
        self.__group_ids = []

    def __del__(self):
        if len(self.__group_ids) > 0:
            print(self.__group_ids)
            print("Error length_heuristic |" + str(__class__))


class SessionCounterTimeWindow(SessionCounter):
    def _compare_length(self, length: int) -> bool:
        return length > self._length_heuristic.max_allowed_time()


class SessionCounterSittingTime(SessionCounter):
    def __init__(self, length_heuristic: LengthHeuristic):
        super().__init__(length_heuristic)
        self.__counter = 0

    def _compare_length(self, length: int) -> bool:
        state = False
        self.__counter += length

        if self.__counter > self._length_heuristic.max_allowed_time():
            state = True
            self.__counter = 0

        return state

    def _increase(self) -> None:
        super()._increase()
        self.__counter = 0

    def _reset(self) -> None:
        super()._reset()
        self.__counter = 0
