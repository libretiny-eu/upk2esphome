#  Copyright (c) Kuba Szczodrzyński 2023-4-21.

import re

import yaml

from upk2esphome.input import parse_input
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


def generate_yaml(config: str, opts: Opts) -> YamlResult:
    from .parts import bulb, module, monitor, netled, static, switch

    parts = [module, static, bulb, switch, netled, monitor]
    yr = YamlResult()

    try:
        config = parse_input(config)
    except ValueError as e:
        yr.error(str(e))
        config = {}

    for part in parts:
        part.generate(yr, config, opts)

    if not yr.found and not yr.errors:
        yr.error(
            "No actual components were added! This means that the type of your device "
            "is not yet supported by this program. This includes for example "
            "thermometers, water leak sensors, or fan controllers."
        )

    yr.text = yaml.dump(yr.data, sort_keys=False)
    yr.text = re.sub(r"'!secret ([\w_]+)'", r"!secret \1", yr.text)
    yr.text = re.sub(r"\n([a-z])", r"\n\n\1", yr.text)
    yr.text = yr.text.replace("'", '"')
    yr.text = yr.text.replace(" {}", "")
    return yr
