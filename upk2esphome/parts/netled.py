#  Copyright (c) Kuba Szczodrzyński 2023-4-21.

from upk2esphome.config import ConfigData
from upk2esphome.generator import invert
from upk2esphome.opts import Opts
from upk2esphome.result import YamlResult


def generate(yr: YamlResult, config: ConfigData, opts: Opts):
    config = config.upk or {}
    keys = ["netled", "netled1", "wfst"]

    netled_reuse = config.get("netled_reuse", None) == 1

    found = False
    for key in keys:
        led_pin = config.get(f"{key}_pin")
        led_inv = config.get(f"{key}_lv", None) == 0
        if led_pin is None:
            continue
        if found:
            yr.warn("Multiple netled pins found!")
            continue
        found = True

        if netled_reuse:
            yr.log(f"Status LED: pin P{led_pin} (shared), inverted {led_inv}")
            light = {
                "platform": "status_led",
                "id": f"light_status",
                "pin": f"P{led_pin}",
            }
            invert(light, led_inv)
            yr.light(light)
        else:
            yr.log(f"Status LED: pin P{led_pin}, inverted {led_inv}")
            status_led = {
                "pin": f"P{led_pin}",
            }
            invert(status_led, led_inv)
            yr.data["status_led"] = status_led
