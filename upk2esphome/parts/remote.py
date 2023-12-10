#  Copyright (c) FIXME Kuba Szczodrzyński 2023-4-21.

from upk2esphome.config import ConfigData
from upk2esphome.generator import invert, pull
from upk2esphome.opts import Opts
from upk2esphome.result import YamlResult


def generate(yr: YamlResult, config: ConfigData, opts: Opts):
    config = config.upk or {}
    in_keys = ["ir", "infrr"]
    out_keys = ["infre"]

    receivers = []

    for key in in_keys:
        ir_pin = config.get(f"{key}")

        # keys current not understood:
        # irfunc
        # irnightt
        # irstep
        # irk*val, irk*fun - presumably these map ir values received to specific functions (light on, off, colours, etc.)

        if ir_pin is None:
            continue

        yr.log(f"Remote receiver: pin P{ir_pin}")
        receiver = {"pin": f"P{ir_pin}", "id": f"P{ir_pin}"}
        pull(receiver, True)
        receiver["_1"] = "dump: all"
        receivers.append(receiver)

    if receivers:
        yr.data["remote_receiver"] = receivers
