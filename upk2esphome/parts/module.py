#  Copyright (c) Kuba Szczodrzyński 2023-4-21.

from upk2esphome.config import ConfigData
from upk2esphome.opts import Opts
from upk2esphome.result import YamlResult

BOARDS = {
    "BK7231T": "generic-bk7231t-qfn32-tuya",
    "BK7231N": "generic-bk7231n-qfn32-tuya",
}


def generate(yr: YamlResult, config: ConfigData, opts: Opts):
    chip_name = config.chip_name
    board = BOARDS.get(chip_name)
    if not board:
        board = "REPLACEME"
        if chip_name:
            yr.warn("Only BK7231T and BK7231N chips are currently supported")
        else:
            yr.warn("No module type found! You have to set the board: manually")
    else:
        yr.log(f"Found {chip_name} config!")

    if opts.esphome_block:
        yr.data["esphome"] = {
            "name": chip_name and f"upk2esphome-{chip_name.lower()}" or "REPLACEME",
        }
        if opts.name_mac:
            yr.data["esphome"]["name_add_mac_suffix"] = True
        yr.data["bk72xx"] = {
            "board": board,
        }
