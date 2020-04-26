import pandas
from .SQLiteDatabase import SQLiteDatabase
from .sql_structure import *
from .sql_data_helper.get_web_mining_rlength import get_length, get_user_id, get_id
from .SessionCounter import SessionCounter


class SessionDatabase(object):
    def load_data(self, input_file: str, stt_seconds: int) -> None:
        self.__drop_structure()
        self.__create_structure()

        df = pandas.read_table(
            input_file,
            header=None,
            names=[
                'ip', 'cookie', 'dtime', 'unixtime', 'request_method', 'url', 'http_version',
                'status_code', 'referrer', 'agent'
            ]
        )
        df.to_sql('web_mining', SQLiteDatabase.connection(), if_exists='append', index=False)
        SQLiteDatabase.connection().commit()

        self.__pos_processing(stt_seconds)

    def length_heuristic(self, session_ounter: SessionCounter) -> None:
        data = SQLiteDatabase.query(get_web_mining_length()).fetchall()

        current_user_id = get_user_id(data[0])

        for item in data:
            if session_ounter.check_user_id(str(get_user_id(item)), str(current_user_id)):
                current_user_id = get_user_id(item)

            session_ounter.add_id(str(get_id(item)))

            session_ounter.check_length(get_length(item))

        SQLiteDatabase.connection().commit()

    def __drop_structure(self) -> None:
        SQLiteDatabase.executescript(drop_tables())

    def __create_structure(self) -> None:
        SQLiteDatabase.executescript(create_tables())

    def __pos_processing(self, stt_seconds: int) -> None:
        SQLiteDatabase.executescript(web_mining_fill_user_id())
        SQLiteDatabase.executescript(web_mining_fill_length(stt_seconds))
