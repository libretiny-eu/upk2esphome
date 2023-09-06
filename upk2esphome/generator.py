#  Copyright (c) Kuba Szczodrzyński 2023-4-21.

import json
import re
from typing import Union

from upk2esphome.config import ConfigData
from upk2esphome.opts import Opts
from upk2esphome.result import YamlResult


def invert(data: dict, inverted: bool, key: str = "pin"):
    if inverted:
        data[key] = {
            "number": data[key],
            "inverted": True,
        }


def pull(data: dict, inverted: bool, key: str = "pin"):
    if inverted:
        data[key] = {
            "number": data[key],
            "inverted": True,
            "mode": "INPUT_PULLUP",
        }
    else:
        data[key] = {
            "number": data[key],
            "mode": "INPUT_PULLDOWN",
        }


def parse_user_param_key(value: str) -> dict | None:
    value = re.sub(r"([^{}\[\]:,]+)", r'"\1"', value)
    value = re.sub(r'"([1-9][0-9]*|0)"', r"\1", value)
    value = re.sub(",}", "}", value)
    value = json.loads(value)
    return value


def parse_raw_data(raw_value: Union[str, dict]) -> dict:
    loaders = [
        json.loads,
        parse_user_param_key,
        dict,
    ]
    if isinstance(raw_value, str):
        raw_value = raw_value.strip()
    value: dict | None = None
    for loader in loaders:
        try:
            value = loader(raw_value)
            break
        except Exception:
            pass
    if not isinstance(value, dict):
        raise ValueError("Input data parsing error")
    return value


def parse_input(
    raw_data: Union[str, dict],
    raw_extras: Union[str, dict],
) -> ConfigData:
    data = parse_raw_data(raw_data)
    extras = parse_raw_data(raw_extras)
    return ConfigData.build(data, extras)


def upk2esphome(
    raw_data: Union[str, dict],
    opts: Opts,
    raw_extras: Union[str, dict] = None,
) -> YamlResult:
    from .parts import bulb, module, monitor, netled, static, switch, tuyamcu

    parts = [module, static, bulb, switch, netled, monitor, tuyamcu]
    yr = YamlResult()

    try:
        # detect input data type
        config = parse_input(raw_data, raw_extras or {})
    except ValueError as e:
        yr.error(str(e))
        return yr

    for part in parts:
        part.generate(yr, config, opts)

    if not config.upk and not config.is_tuya_mcu:
        # unknown type
        yr.error(
            "The chosen device doesn't contain pin configuration.\n\n"
            "Possible causes:\n"
            "- it has vendor-specific firmware\n"
            "- it uses TuyaMCU (report error if that's the case!)\n\n"
            "Auto-generating ESPHome YAML is not possible."
        )
        yr.data = {}

    if not yr.found and not yr.errors:
        yr.error(
            "No actual components were added!\n"
            "This means that **valid configuration has been found**,\n"
            "but this type of device is not yet supported by this program.\n"
            "This includes for example thermometers, water leak sensors, "
            "or fan controllers."
        )

    if yr.errors:
        yr.logs = []
        yr.warnings = []

    yr.config = config
    return yr
