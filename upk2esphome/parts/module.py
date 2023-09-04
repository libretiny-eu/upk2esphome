#  Copyright (c) Kuba Szczodrzyński 2023-4-21.

from upk2esphome.config import ConfigData
from upk2esphome.opts import Opts
from upk2esphome.result import YamlResult

BOARDS = {
    "WB": "generic-bk7231t-qfn32-tuya",
    "CB": "generic-bk7231n-qfn32-tuya",
    "BK7231T": "generic-bk7231t-qfn32-tuya",
    "BK7231N": "generic-bk7231n-qfn32-tuya",
}


def generate(yr: YamlResult, config: ConfigData, opts: Opts):
    module = config.upk.get("module", "")
    chip = config.profile.get("name", "").rpartition(" ")[2]

    board = BOARDS.get(chip, BOARDS.get(module[0:2], None))
    if not board:
        board = "REPLACEME"
        if module or chip:
            yr.warn("Only BK7231T and BK7231N chips are currently supported")
        else:
            yr.warn("No module type found! You have to set the board: manually")
    else:
        yr.log(f"Found {module or chip} config!")

    if opts.esphome_block:
        yr.data["esphome"] = {
            "name": f"upk2esphome-{(module or chip).lower()}",
        }
        if opts.name_mac:
            yr.data["esphome"]["name_add_mac_suffix"] = True
        yr.data["bk72xx"] = {
            "board": board,
        }
