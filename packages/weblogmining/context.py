import os.path as path
from typing import Dict, List
from .CleanUpData import CleanUpData
from .database import SessionDatabase, SQLiteDatabase, STTQLengthHeuristic, RLengthHeuristic, SLengthLengthHeuristic, \
    SessionCounterTimeWindow, SessionCounterSittingTime, PostProcessingDatabase

__all__ = ['clean_up_data', 'session_identifier']


def clean_up_data(input_file_name: str, output_file_name: str) -> None:
    cleanup = CleanUpData(input_file_name, output_file_name)
    cleanup.run()


def init_sqlite(dir_name: str) -> None:
    SQLiteDatabase.set_db_location(
        path.normpath(
            path.join(
                dir_name,
                'sqlite.db'
            )
        )
    )


def session_identifier(input_file_name: str, stt_q: float, stt_seconds: int = 3600, navigation_ratio: float = 0.4,
                       estimate_time: int = 600) -> None:
    session_database = SessionDatabase()
    session_database.load_data(input_file_name, stt_seconds)
    session_database.length_heuristic(SessionCounterTimeWindow(RLengthHeuristic(navigation_ratio)))
    session_database.length_heuristic(SessionCounterTimeWindow(STTQLengthHeuristic(stt_q)))
    session_database.length_heuristic(SessionCounterSittingTime(SLengthLengthHeuristic(estimate_time)))


def postprocessing_data(entry_role: Dict[str, List[str]], default_entry_role: str) -> None:
    postprocessing = PostProcessingDatabase()
    postprocessing.run(entry_role, default_entry_role)
