#  Copyright (c) Kuba Szczodrzyński 2023-4-21.

from upk2esphome.result import YamlResult


def generate(yr: YamlResult, config: dict):
    if "module" in config:
        module = config["module"]
    else:
        yr.warn("No module type found! You have to set the board: manually")
        yr.data["esphome"] = {
            "name": "UPK2ESPHome",
            "name_add_mac_suffix": True,
        }
        yr.data["libretuya"] = {
            "board": "FIX_ME",
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

    yr.data["esphome"] = {
        "name": config["module"],
        "name_add_mac_suffix": True,
    }
    yr.data["libretuya"] = {
        "board": board,
        "framework": {
            "version": "dev",
        },
    }
