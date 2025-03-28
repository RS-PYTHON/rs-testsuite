import json


def check_json_path_is_not_null(data: json, item1: str, item2: str):
    """Checks that path item1.item2 is found in json data"""
    assert (
        data[item1][item2] is not None
    ), f"Path {item1}.{item2} can not be found on json {data}."


def is_valid_json(chain: str) -> bool:
    """Checks that json is valid"""
    result = json.loads(chain, strict=False)
    return isinstance(result, (dict, list))
