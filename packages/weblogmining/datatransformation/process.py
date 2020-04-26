from typing import Optional, Dict
from .basedata import *
from .helper import elements as el


def process_base_data(line: str) -> Optional[Dict[str, str]]:
    line = clean_up(line)

    status_code = get_status_code(line)
    if check_status_code(status_code):
        return None

    user_data = get_user_data(line)
    if check_user_data(user_data):
        return None

    request_data = get_request_data(user_data)
    if check_request_data(request_data):
        return None

    elements = re.split(r'\s+', line)

    date_time = re.sub('\[|\]', '', elements[2] + ' (' + elements[3] + ')')

    return {
        'IP': elements[0],
        'Cookie': elements[1],
        'DTime': date_time,
        'Unixtime': str(get_unixtime(date_time, get_datetime_format())),
        'RequestMethod': request_data[0],
        'URL': request_data[1],
        'Version': request_data[2],
        'StatusCode': status_code,
        'Referrer': user_data[1],
        'Agent': user_data[2]
    }


def process_pre_robots(line: str) -> Optional[Dict[str, str]]:
    elements = el.get_elements_transform_file(line)
    if not re.search(r'robot[s]?\.txt', el.get_url(elements)) and not re.search(r'(?i)(bot)|(spider)|(craw)', el.get_agent(elements)):
        return None

    return {
        'IP': el.get_ip(elements),
        'URL': el.get_cookie(elements),
        'Agent': el.get_agent(elements)
    }


def process_robots(line: str, ip: list, agent: list) -> bool:
    elements = el.get_elements_transform_file(line)
    if el.get_ip(elements) in ip or el.get_agent(elements) in agent:
        return True

    return False
