#  Copyright (c) Peter van Dijk 2025-2-8.

from upk2esphome.config import ConfigData
from upk2esphome.generator import invert, pull
from upk2esphome.opts import Opts
from upk2esphome.result import YamlResult


def generate(yr: YamlResult, config: ConfigData, opts: Opts):
    config = config.upk or {}
    keys = [
        "key_pin",
        "k2pin_pin",
        "k3pin_pin",
    ]
    if not any(key in config for key in keys):
        return
    yr.log("Key config")

    keys = []
    for i in range(1, 10):
        if i == 1:
            name = "key"
        else:
            name = f"k{i}pin"

        k_pin = config.get(f"{name}_pin", None)
        k_inv = config.get(f"{name}_lv", None) == 0

        if k_pin is not None:
            yr.log(f" - key {i}: pin P{k_pin}")
            binary = {
                "platform": "gpio",
                "id": f"binary_switch_{i}",
                "pin": f"P{k_pin}",
                "on_press": {
                    "then": [],
                },
            }
            pull(binary, k_inv)
            yr.binary(binary)
