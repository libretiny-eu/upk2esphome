#  Copyright (c) Kuba Szczodrzyński 2025-12-29.

from typing import Any

KEY_MAP = {
    "sw_": "",
    "_value": "",
    # monitor
    "dltj_ct": "chip_type",
    "dltj_ivcpin_pin": "sel_pin_pin",
    "dltj_ivcpin_lv": "sel_pin_lv",
    "dltj_ivpin_pin": "vi_pin",
    "dltj_epin_pin": "ele_pin",
    "dltj_ri": "resistor",
    # switch
    "ch_0_bt": "bt1",
    "ch_1_bt": "bt2",
    "ch_2_bt": "bt3",
    "ch_3_bt": "bt4",
    "ch_0_rl": "rl1",
    "ch_1_rl": "rl2",
    "ch_2_rl": "rl3",
    "ch_3_rl": "rl4",
    "net_wfst": "netled",
}

VALUE_MAP = {
    True: 1,
    False: 0,
    "true": 1,
    "false": 0,
}


def flatten_dict(key: str, value: Any, out: dict) -> dict:
    if isinstance(value, dict):
        for k, v in value.items():
            flatten_dict(f"{key}_{k}" if key else k, v, out)
    elif isinstance(value, list):
        for k, v in enumerate(value):
            flatten_dict(f"{key}_{k}" if key else k, v, out)
    else:
        out[key] = value
    return out


def upk_old2new(upk: dict) -> dict:
    upk = flatten_dict(key="", value=upk, out={})

    for k, v in dict(upk).items():
        del upk[k]
        for item, repl in KEY_MAP.items():
            if k.startswith(item):
                k = repl + k[len(item) :]
            if k.endswith(item):
                k = k[: -len(item)] + repl
            if k == item:
                k = repl
        v = VALUE_MAP.get(v, v)
        upk[k] = v

    return dict(sorted(upk.items()))
