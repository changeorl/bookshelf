import json
from datetime import date, datetime


def bold(text):
    return f"\033[1m{text}\033[0m"


def italic(text):
    return f"\033[3m{text}\033[0m"


def bold_italic(text):
    return f"\033[1m\033[3m{text}\033[0m"


def timenow():
    """
    return current time in format HH:MM:SS
    """
    return datetime.now().strftime("%H:%M:%S")


def today():
    """
    return current date in format YYYY-MM-DD
    """
    return date.today()


def aprint(input_dict: dict, comma=False):
    """
    print a dict in aligned format

    :param input_dict: dict to be printed
    :param comma: aligned comma or not
    :return: None

    e.g.
    >>> aprint({"a": 1, "bb": 2, "ccc": 3})
    a:   1
    bb:  2
    ccc: 3
    """
    max_key_length = max(len(key) for key in input_dict.keys())
    for key, value in input_dict.items():
        if not comma:
            key += ":"
            formatted_key = f"{key:{max_key_length + 1}}"
            print(f"{formatted_key} {value}")
        else:
            formatted_key = f"{key:{max_key_length}}"
            print(f"{formatted_key}: {value}")


def jprint(input_dict: dict, indent: int = 4):
    """
    print a dict in json format

    :param input_dict: dict to be printed
    :param indent: indent of json format
    :return: None

    e.g.
    >>> jprint({"a": 1, "bb": 2, "ccc": 3})
    {
        "a": 1,
        "bb": 2,
        "ccc": 3
    }
    """
    print(json.dumps(input_dict, indent=4, ensure_ascii=False))


def jsave(input_dict: dict, indent: int = 4, local_dir="data.json"):
    """
    print a dict in json format and save to a file

    :param input_dict: dict to be printed
    :param indent: indent of json format
    :param local_dir: file path
    :return: None

    e.g.
    >>> jsave({"a": 1, "bb": 2, "ccc": 3})
    > data.json
    {
        "a": 1,
        "bb": 2,
        "ccc": 3
    }
    """
    with open(local_dir, "w+") as f:
        json.dump(input_dict, f, indent=4, ensure_ascii=False)
    print(f"@jsave to {local_dir}")


def lprint(input_list, right: bool = False, index: bool = True):
    """
    print a list in aligned format

    :param list: list to be printed
    :param right: right align or left align
    :param index: print index or not
    :return: None

    e.g.
    >>> lprint(["a", "bb", "ccc"])
    0 a
    1 bb
    2 ccc
    """
    max_index_width = len(str(len(input_list) - 1))
    max_item_width = max(len(str(item)) for item in input_list)
    for i, item in enumerate(input_list):
        item_str = (
            str(item).rjust(max_item_width)
            if right
            else str(item).ljust(max_item_width)
        )

        if index:
            index_str = str(i).ljust(max_index_width)
            print(f"{index_str} {item_str}")
        else:
            print(item_str)
