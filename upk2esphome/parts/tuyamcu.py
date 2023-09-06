#  Copyright (c) Kuba Szczodrzyński 2023-9-4.

from upk2esphome.config import ConfigData
from upk2esphome.datapoints import Datapoint, convert_all
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

    model = config.model
    model_id = model.get("modelId", None)
    schema_id = config.schema_id
    services = model.get("services", None)
    if not model_id or not isinstance(services, list):
        yr.warn("Invalid schema model structure: missing 'modelId' or 'services'")
        yr.needs_tuyamcu_model = True
        return

    if schema_id and model_id != schema_id:
        yr.warn(
            f"Downloaded schema ID ({model_id}) "
            f"doesn't match device schema ID ({schema_id})"
        )
        yr.needs_tuyamcu_model = True
        return

    yr.data["tuya"] = {
        "_1": f"DPIDs processed from schema model: {model_id}",
    }

    # mark 'found' only if supported DP component was processed
    yr.found = False
    dps: list[Datapoint] = []
    for service in services:
        for dp_data in service.get("properties", []):
            dps.append(Datapoint.build(dp_data))

    convert_all(yr, config, opts, dps)
