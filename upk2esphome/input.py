#  Copyright (c) Kuba Szczodrzyński 2023-4-21.

import json
import re
from typing import Union


def parse_user_param_key(value: str) -> dict | None:
    value = re.sub(r"([^{}\[\]:,]+)", r'"\1"', value)
    value = re.sub(r'"([1-9][0-9]*|0)"', r"\1", value)
    value = re.sub(",}", "}", value)
    value = json.loads(value)
    return value


def parse_input(data: Union[str, dict]) -> dict:
    if isinstance(data, str):
        data = data.strip()
    loaders = [
        json.loads,
        parse_user_param_key,
        dict,
    ]

    value: dict | None = None
    for loader in loaders:
        try:
            value = loader(data)
            break
        except Exception:
            pass

    if not isinstance(value, dict):
        raise ValueError("Input format unrecognized")

    if "device_configuration" in value:
        value = value["device_configuration"]
    elif "schemas" in value:
        raise ValueError(
            "The specified Cloudcutter JSON doesn't contain device configuration"
        )

    if "user_param_key" in value:
        value = value["user_param_key"]
    elif "gw_bi" in value:
        raise ValueError(
            "The specified storage JSON doesn't contain device configuration"
        )

    if "Jsonver" in value or "jv" in value or "crc" in value:
        value = dict(sorted(value.items()))
        return value

    raise ValueError("JSON value found, but the config is missing")
