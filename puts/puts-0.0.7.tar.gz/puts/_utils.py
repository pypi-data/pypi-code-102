from datetime import date, datetime, time
from typing import Callable, Dict, Union

##############################################################################
### Conversion between 'datetime' and 'date' objects


def convert_date_to_datetime(date_obj: date) -> datetime:
    """
    Convert a datetime.date object to a datetime.datatime object
    Return: datetime
    Exception: AssertionError
    """
    if isinstance(date_obj, datetime):
        return date_obj
    # REF: https://stackoverflow.com/a/11619200
    assert isinstance(date_obj, date), "Not a date object."
    # return the original value if the input is a datetime object
    if isinstance(date_obj, datetime):
        return date_obj
    return datetime.combine(date_obj, time())


def convert_datetime_to_date(datetime_obj: datetime) -> date:
    """
    Convert a datetime.datatime object to a datetime.date object
    Return: datetime
    Exception: AssertionError
    """
    if isinstance(datetime_obj, date):
        return datetime_obj
    assert isinstance(datetime_obj, datetime), "Not a datetime object."
    return datetime_obj.date()


##############################################################################
### Json Serialization for 'datetime' or 'date objects


def json_serial(obj: Union[datetime, date]) -> str:
    """
    JSON serializer for objects not serializable by default json code

    Example Usage:
        >>> import json
        >>> x = {"time": datetime.now()}
        >>> print(json.dumps(x, indent=4, default=json_serial))

    Raises:
        TypeError
    """
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


##############################################################################
### Color printers


def _colorcode(code: int) -> str:
    return "\033[" + str(code) + "m"


_RED = _colorcode(31)
_GREEN = _colorcode(32)
_YELLOW = _colorcode(33)
_CYAN = _colorcode(36)
_WHITE = _colorcode(37)
_BOLD = _colorcode(1)
_RESET = _colorcode(0)


def print_green(string: str, bold=False) -> None:
    print(f"{_BOLD if bold else ''}{_GREEN}{string}{_RESET}")


def print_yellow(string: str, bold=False) -> None:
    print(f"{_BOLD if bold else ''}{_YELLOW}{string}{_RESET}")


def print_red(string: str, bold=False) -> None:
    print(f"{_BOLD if bold else ''}{_RED}{string}{_RESET}")


def print_cyan(string: str, bold=False) -> None:
    print(f"{_BOLD if bold else ''}{_CYAN}{string}{_RESET}")


def print_bold(string: str, bold=True) -> None:
    print(f"{_BOLD if bold else ''}{string}{_RESET}")


def print_with_color(
    *args, color: str = "green", bold: bool = False, sep: str = " "
) -> None:
    """
    print to console with specified color

    Args:
        string: str
            The string you want to print
        color: str
            one of the options: "green", "yellow", "cyan", "red"
            alternatively: "g", "y", "c", "r"
        bold: bool
            Whether to print in bold
    """
    assert isinstance(sep, str)
    targets = [str(x) for x in args]
    string = sep.join(targets)

    color = str(color).lower()
    color_printer_map: Dict[str, Callable] = {
        "green": print_green,
        "g": print_green,
        "yellow": print_yellow,
        "y": print_yellow,
        "red": print_red,
        "r": print_red,
        "cyan": print_cyan,
        "c": print_cyan,
    }
    if color in color_printer_map:
        color_print = color_printer_map[color]
        color_print(string=string, bold=bold)
    else:
        print_bold(string=string, bold=bold)
    return


printc = print_with_color

if __name__ == "__main__":
    printc("Hello,", "World!", color="yellow", bold=True)
