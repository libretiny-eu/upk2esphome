#  Copyright (c) Kuba Szczodrzyński 2023-9-6.

import json
from pathlib import Path

from upk2esphome import ConfigData, Opts, YamlResult
from upk2esphome.datapoints.model import Datapoint


def convert_all(yr: YamlResult, config: ConfigData, opts: Opts, dps: list[Datapoint]):
    from upk2esphome.datapoints.category import base

    categories = dict(
        # dlq=dlq,
    )
    converter = categories.get(config.category, None)
    converters = [base]
    if converter:
        converters.insert(0, converter)

    mapping = {}
    mapping_path = Path(__file__).parent.joinpath("mapping")
    category_path = Path(__file__).parent.joinpath(
        "category", f"{config.category}.json"
    )
    for path in mapping_path.glob("*.json"):
        mapping |= json.loads(path.read_text("utf-8"))
    if category_path.is_file():
        mapping |= json.loads(category_path.read_text("utf-8"))

    for dp in dps:
        for converter in converters:
            match dp.mode:
                case "ro":
                    if converter.process_ro(yr, opts, dp, mapping):
                        break
                case "rw":
                    if converter.process_rw(yr, opts, dp, mapping):
                        break
            conv_name = converter.__name__.rpartition(".")[2]
            yr.warn(f"Converter '{conv_name}' couldn't process {dp.info}")
