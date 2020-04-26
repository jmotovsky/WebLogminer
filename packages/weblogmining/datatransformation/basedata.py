import re, pytz, datetime, calendar
from .helper.exception import StatusCodeException, UserDataException, RequestDataException


def clean_up(input_data: str) -> str:
    input_data = remove_trash(input_data)

    return input_data


def remove_trash(input_data: str) -> str:
    return re.sub('\s+[q]+', '', input_data)


def get_status_code(input_data: str) -> str:
    status_code = re.search(r'"\s*([\d]+\s*)+"', input_data)

    if not status_code:
        raise StatusCodeException(input_data)

    status_code = re.search(r'[^\d]\d{3}[^\d]', status_code.group(0))

    if not status_code:
        raise StatusCodeException(input_data)

    status_code = re.sub(r'"|\s+', '', status_code.group(0))

    if not status_code.isdigit():
        raise StatusCodeException(input_data)

    return status_code


def check_status_code(status_code: str) -> bool:
    return int(status_code) >= 400


def get_user_data(input_data: str) -> list:
    user_data = re.findall(r'"((?:[^"\\]|\\.)*)"', input_data)
    if not len(user_data) == 3:
        raise UserDataException(input_data)

    return user_data


def check_user_data(input_data: list) -> bool:
    return False


def get_request_data(input_data: list) -> list:
    data = input_data[0].split()
    if not len(data) == 3:
        raise RequestDataException(input_data)

    if input_data[0] == '-':
        raise RequestDataException(input_data)

    return data


def check_request_data(input_data: list) -> bool:
    if not input_data[0].startswith('GET'):
        return True

    if re.search(r'(?<!robots)\.(?!(php)|(htm))[a-z]{2,4}($|\?)', input_data[1]):
        return True

    return False


def get_unixtime(date_time: str, dt_format: str) -> int:
    return calendar.timegm(datetime.datetime.strptime(date_time, dt_format).astimezone(pytz.utc).timetuple())


def get_datetime_format() -> str:
    return "%d/%b/%Y:%H:%M:%S (%z)"
