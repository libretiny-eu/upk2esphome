#  Copyright (c) Kuba Szczodrzyński 2023-4-21.

from upk2esphome.opts import Opts
from upk2esphome.result import YamlResult


def generate(yr: YamlResult, config: dict, opts: Opts):
    if "module" in config:
        module = config["module"]
    else:
        yr.warn("No module type found! You have to set the board: manually")
        if opts.esphome_block:
            yr.data["esphome"] = {
                "name": "upk2esphome",
            }
            if opts.name_mac:
                yr.data["esphome"]["name_add_mac_suffix"] = True
            yr.data["bk72xx"] = {
                "board": "REPLACEME",
                "framework": {
                    "version": "dev",
                },
            }
        return

    match module[0:2].upper():
        case "WB":
            board = "generic-bk7231t-qfn32-tuya"
        case "CB":
            board = "generic-bk7231n-qfn32-tuya"
        case _:
            yr.warn("Only BK7231T and BK7231N chips are currently supported")
            return

    yr.log(f"Found {module} config!")

    if opts.esphome_block:
        yr.data["esphome"] = {
            "name": config["module"].lower(),
        }
        if opts.name_mac:
            yr.data["esphome"]["name_add_mac_suffix"] = True
        yr.data["bk72xx"] = {
            "board": board,
            "framework": {
                "version": "dev",
            },
        }
