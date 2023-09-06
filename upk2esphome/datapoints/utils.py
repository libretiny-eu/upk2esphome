#  Copyright (c) Kuba Szczodrzyński 2023-9-6.

import re
from typing import Any

from upk2esphome import Opts, YamlResult
from upk2esphome.datapoints.model import Datapoint


def get_dict_mapping(mapping: dict, value: str) -> dict:
    while isinstance(value, str) and value in mapping:
        value = mapping[value]
    if isinstance(value, dict):
        return value
    return {}


def get_str_mapping(mapping: dict, value: str) -> str:
    orig_value = value
    while isinstance(value, str) and value in mapping:
        value = mapping[value]
    if isinstance(value, str):
        return value
    return orig_value


def get_mapping(
    yr: YamlResult,
    opts: Opts,
    dp: Datapoint,
    mapping: dict,
) -> dict:
    if dp.code in mapping:
        return get_dict_mapping(mapping, dp.code)
    yr.warn(f"Missing mapping for {dp.info}")
    name = dp.code.replace("_", " ").replace("-", " ").title()
    return dict(
        name=f"(Unconfirmed) {name}",
    )


def get_unit(
    yr: YamlResult,
    opts: Opts,
    dp: Datapoint,
    mapping: dict,
) -> dict:
    if dp.spec.unit:
        unit = dp.spec.unit
        if unit in mapping:
            unit = get_str_mapping(mapping, unit)
        else:
            unit = re.sub(r"[^\x20-\x7F]", "", unit)
        return dict(unit_of_measurement=unit)
    return dict()


def add_filter(component: dict, name: str, value: Any):
    if "filters" not in component:
        component["filters"] = []
    component["filters"].append({name: value})
