import datetime

FORMAT_STRING = "%b %d %Y %H"
FORMAT_STRING_LEN = len("Jan 01 2000 23")  # Also : +0


def parse_time_str(time_str):
    return datetime.datetime.strptime(
        time_str[:FORMAT_STRING_LEN], FORMAT_STRING
    )
