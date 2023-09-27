#  Copyright (c) Kuba Szczodrzyński 2023-4-21.

from upk2esphome.config import ConfigData
from upk2esphome.generator import invert, pull
from upk2esphome.opts import Opts
from upk2esphome.result import YamlResult


def generate(yr: YamlResult, config: ConfigData, opts: Opts):
    config = config.upk or {}
    keys = [
        "bt1_pin",
        "bt2_pin",
        "bt3_pin",
        "bt4_pin",
        "total_bt_pin",
        "rl1_pin",
        "rl2_pin",
        "rl3_pin",
        "rl4_pin",
        "rl_type",
        "onoff1",
    ]
    if not any(key in config for key in keys):
        return
    yr.log("Switch/plug config")

    netled_reuse = config.get("netled_reuse", None) == 1

    switches = []
    for i in range(0, 10):
        rl_pin = config.get(f"rl{i}_pin", None)
        rl_inv = config.get(f"rl{i}_lv", None) == 0
        led_pin = config.get(f"led{i}_pin", None)
        led_inv = config.get(f"led{i}_lv", None) == 0
        bt_pin = config.get(f"bt{i}_pin", None)
        bt_inv = config.get(f"bt{i}_lv", None) == 0
        onoff_pin = config.get(f"onoff{i}", None)
        if rl_pin is None:
            continue

        yr.log(f" - relay {i}: pin P{rl_pin}")
        yr.found = True
        switch = {
            "platform": "gpio",
            "id": f"switch_{i}",
            "name": f"Relay {i}",
            "pin": f"P{rl_pin}",
        }
        invert(switch, rl_inv)

        if led_pin is not None and netled_reuse:
            yr.warn(
                f"Skipping LED {i} on pin P{led_pin} - shared status LED is enabled"
            )
            led_pin = None

        if led_pin is not None:
            yr.log(f" - LED {i}: pin P{led_pin}")
            output = {
                "platform": "libretiny_pwm",
                "id": f"output_led_{i}",
                "pin": f"P{led_pin}",
            }
            invert(output, led_inv)
            yr.output(output)
            light = {
                "platform": "monochromatic",
                "id": f"light_switch_{i}",
                "output": output["id"],
            }
            yr.light(light)
            switch["on_turn_on"] = [
                {"light.turn_on": light["id"]},
            ]
            switch["on_turn_off"] = [
                {"light.turn_off": light["id"]},
            ]
        elif netled_reuse:
            yr.log(f" - LED {i}: (shared)")
            switch["on_turn_on"] = [
                {"light.turn_on": "light_status"},
            ]
            switch["on_turn_off"] = [
                {"light.turn_off": "light_status"},
            ]

        if bt_pin is not None:
            yr.log(f" - button {i}: pin P{bt_pin}")
            binary = {
                "platform": "gpio",
                "id": f"binary_switch_{i}",
                "pin": f"P{bt_pin}",
                "on_press": {
                    "then": [
                        {"switch.toggle": switch["id"]},
                    ],
                },
            }
            pull(binary, bt_inv)
            yr.binary(binary)

        if onoff_pin is not None:
            yr.log(f" - ON/OFF switch {i}: pin P{onoff_pin}")
            binary = {
                "platform": "gpio",
                "id": f"binary_onoff_{i}",
                "pin": f"P{onoff_pin}",
                "on_state": {
                    "then": [
                        {"switch.toggle": switch["id"]},
                    ],
                },
            }
            pull(binary, inverted=True)
            yr.binary(binary)

        switches.append(switch["id"])
        yr.switch(switch)

    bt_pin = config.get(f"total_bt_pin", None)
    bt_inv = config.get(f"total_bt_lv", None) == 0
    if bt_pin is not None:
        yr.log(f" - all-toggle button: pin P{bt_pin}")
        yr.found = True
        binary = {
            "platform": "gpio",
            "id": f"binary_switch_all",
            "pin": f"P{bt_pin}",
            "on_press": {"then": []},
        }
        pull(binary, bt_inv)
        for switch in switches:
            binary["on_press"]["then"].append({"switch.toggle": switch})
        yr.binary(binary)
