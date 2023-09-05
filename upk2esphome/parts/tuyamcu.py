#  Copyright (c) Kuba Szczodrzyński 2023-9-4.

from upk2esphome.config import ConfigData
from upk2esphome.opts import Opts
from upk2esphome.result import YamlResult


def generate(yr: YamlResult, config: ConfigData, opts: Opts):
    if not config.is_tuya_mcu:
        return

    yr.log("Found TuyaMCU device")

    baud_rate = config.uart_config.get("uart_baud", None) or config.uart_config.get(
        "baud", None
    )
    if not baud_rate:
        baud_rate = "REPLACEME"
        yr.warn(
            "TuyaMCU baud rate not found!\n"
            "You need to adjust it manually: in most cases, use either 9600 or 115200"
        )

    yr.data["uart"] = {
        "rx_pin": "RX1",
        "tx_pin": "TX1",
        "baud_rate": baud_rate,
    }
    yr.data["tuya"] = {}
    yr.found = True

    if not config.model:
        yr.warn("No schema model for TuyaMCU - can't process datapoints")
        yr.needs_tuyamcu_model = True
        return
