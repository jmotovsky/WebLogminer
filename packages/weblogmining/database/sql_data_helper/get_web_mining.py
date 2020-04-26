def get_id(data: tuple) -> int:
    return data[0]


def get_user_id(data: tuple) -> int:
    return data[1]


def get_session_id_rlength(data: tuple) -> int:
    return data[2]


def get_session_id_sttq(data: tuple) -> int:
    return data[3]


def get_session_id_slength(data: tuple) -> int:
    return data[4]


def get_session_ip(data: tuple) -> str:
    return data[5]


def get_session_cookie(data: tuple) -> str:
    return data[6]


def get_session_dtime(data: tuple) -> str:
    return data[7]


def get_unixtime(data: tuple) -> int:
    return data[8]


def get_hours(data: tuple) -> int:
    return data[9]


def get_week_day(data: tuple) -> int:
    return data[10]


def get_length(data: tuple) -> int:
    return data[11]


def get_request_method(data: tuple) -> str:
    return data[12]


def get_url(data: tuple) -> str:
    return data[13]


def get_category(data: tuple) -> str:
    return data[14]


def get_entry(data: tuple) -> str:
    return data[15]


def get_http_version(data: tuple) -> str:
    return data[16]


def get_status_code(data: tuple) -> int:
    return data[17]


def get_referrer(data: tuple) -> str:
    return data[18]


def get_agent(data: tuple) -> str:
    return data[19]
