import re
from typing import Dict, List
from .SQLiteDatabase import SQLiteDatabase
from .sql_structure import *
from .sql_data_helper.get_web_mining import get_url, get_id, get_session_ip


class PostProcessingDatabase(object):
    def run(self, entry_role: Dict[str, List[str]], default_entry_role: str) -> None:
        SQLiteDatabase.executescript(update_datetime_data())

        data = SQLiteDatabase.query(get_web_mining()).fetchall()
        for item in data:
            id = get_id(item)
            ip = get_session_ip(item)
            category = get_url(item).split('/')[1]

            if category and not re.search(r'(\.((php)|(htm)))|(\?)', category):
                SQLiteDatabase.query(update_web_mining_category(category, id))

            SQLiteDatabase.query(update_web_mining_entry(self.__find_entry(ip, entry_role, default_entry_role), id))

        SQLiteDatabase.connection().commit()

    def __find_entry(self, ip: str, entry_role: Dict[str, List[str]], default_entry_role: str) -> str:
        entry: str = ''
        for entry_name, values in entry_role.items():
            for pattern in values:
                if self.__check_entry_pattern(ip, pattern):
                    entry = entry_name
                    break
            if entry:
                break

        if not entry:
            entry = default_entry_role

        return entry

    def __check_entry_pattern(self, ip: str, pattern: str) -> bool:
        if len(ip) == len(pattern) and self.__transform_ip(ip, pattern) == ip:
            return True
        else:
            return False

    def __transform_ip(self, ip: str, pattern: str) -> str:
        for c in range(0, len(ip)):
            if pattern[c] == '*':
                pattern = pattern.replace(pattern[c], ip[c], 1)

        return pattern
