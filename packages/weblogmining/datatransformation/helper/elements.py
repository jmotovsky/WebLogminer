import re


def get_ip(elements: list) -> str:
    return elements[0]


def get_cookie(elements: list) -> str:
    return elements[1]


def get_dtime(elements: list) -> str:
    return elements[2]


def get_unixtime(elements: list) -> str:
    return elements[3]


def get_request_method(elements: list) -> str:
    return elements[4]


def get_url(elements: list) -> str:
    return elements[5]


def get_version(elements: list) -> str:
    return elements[6]


def get_status_code(elements: list) -> str:
    return elements[7]


def get_referrer(elements: list) -> str:
    return elements[8]


def get_agent(elements: list) -> str:
    return elements[9]


def get_elements_transform_file(line: str) -> list:
    return re.split(r'\t', line)
