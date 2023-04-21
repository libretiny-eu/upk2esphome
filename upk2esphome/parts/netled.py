#  Copyright (c) Kuba Szczodrzyński 2023-4-21.

from upk2esphome.generator import invert
from upk2esphome.result import YamlResult


def generate(yr: YamlResult, config: dict):
    keys = ["netled", "netled1", "wfst"]

    found = False
    for key in keys:
        led_pin = config.get(f"{key}_pin")
        led_inv = config.get(f"{key}_pin", None) == 0
        if led_pin is None:
            continue
        if found:
            yr.warn("Multiple netled pins found!")
            continue
        found = True

        yr.log(f"Status LED: pin P{led_pin}, inverted {led_inv}")
        status_led = {
            "pin": f"P{led_pin}",
        }
        invert(status_led, led_inv)
        yr.data["status_led"] = status_led
