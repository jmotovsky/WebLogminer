import sqlite3, os
from typing import Optional


class SQLiteDatabase(object):
    __instance = None
    __db_locatiom = os.path.normpath(os.path.join(os.environ['PWD'],'sqlite.db'))

    @staticmethod
    def _instance():
        if __class__.__instance is None:
            __class__.__instance = __class__()

        return __class__.__instance

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)

            try:
                print('connecting to SQLite database ... ' + cls.__db_locatiom)
                __class__.__instance.__connection = sqlite3.connect(cls.__db_locatiom)
                __class__.__instance.__cursor = __class__.__instance.__connection.cursor()
                __class__.__instance.__cursor.execute('SELECT sqlite_version()')
                db_version = __class__.__instance.__cursor.fetchone()

            except Exception as error:
                print('Error: connection not established {}'.format(error))
                __class__.__instance = None

            else:
                print('connection established DB version {}'.format(db_version[0]))

        return cls.__instance

    @staticmethod
    def set_db_location(new_db_location: str) -> None:
        __class__.__db_locatiom = os.path.normpath(os.path.join(os.environ['PWD'], new_db_location))

    @staticmethod
    def connection() -> sqlite3.Connection:
        return __class__._instance().__connection

    @staticmethod
    def cursor() -> sqlite3.Cursor:
        return __class__.connection().cursor()

    @staticmethod
    def query(query: str) -> Optional[sqlite3.Cursor]:
        try:
            result = __class__.cursor().execute(query)
        except Exception as error:
            print('error execting query "{}", error: {}'.format(query, error))
            return None
        else:
            return result

    @staticmethod
    def executescript(sql_script: str) -> None:
        __class__.connection().executescript(sql_script)
        __class__.connection().commit()

    def __del__(self):
        __class__.connection().commit()
        __class__.cursor().close()
        __class__.connection().close()
