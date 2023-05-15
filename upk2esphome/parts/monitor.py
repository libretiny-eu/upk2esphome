#  Copyright (c) Kuba Szczodrzyński 2023-4-21.

from upk2esphome.generator import invert
from upk2esphome.opts import Opts
from upk2esphome.result import YamlResult


def generate(yr: YamlResult, config: dict, opts: Opts):
    keys = [
        "chip_type",
        "over_cur",
        "over_vol",
        "lose_vol",
        "ele_pin",
        "vi_pin",
        "sel_pin_pin",
        "sel_pin_lv",
        "sample_resistor",
        "work_voltage",
        "vol_def",
    ]
    if not any(key in config for key in keys):
        return
    if "chip_type" not in config:
        yr.warn("Found some power monitoring keys, but no chip_type!")
        return

    resistor = config.get("sample_resistor", None)
    resistor = config.get("resistor", resistor)
    chip_type = config["chip_type"]
    match chip_type:
        case 0 | 1:  # BL0937 |  HLW8012
            ele_pin = config.get("ele_pin", None)
            vi_pin = config.get("vi_pin", None)
            sel_pin = config.get("sel_pin_pin", None)
            sel_inv = config.get("sel_pin_lv", None) == 1
            chip = "BL0937" if chip_type == 0 else "HLW8012"
            yr.log(
                f"Power monitoring chip {chip}: "
                f"CF/ELE=P{ele_pin}, CF1/VI=P{vi_pin}, SEL={sel_pin}"
            )
            yr.found = True
            sensor = {
                "platform": "hlw8012",
                "model": chip,
                "cf_pin": f"P{ele_pin}",
                "cf1_pin": f"P{vi_pin}",
                "sel_pin": f"P{sel_pin}",
                "current": {"name": f"{chip} Current"},
                "voltage": {"name": f"{chip} Voltage"},
                "power": {"name": f"{chip} Power"},
                "energy": {"name": f"{chip} Energy"},
                "voltage_divider": 1600,
            }
            if resistor is not None:
                yr.log(f" - shunt resistor: {resistor} mΩ")
                sensor["current_resistor"] = f"{resistor/1000:.03f} ohm"
            invert(sensor, sel_inv, "sel_pin")
            invert(sensor, chip_type == 0, "cf_pin")
            invert(sensor, chip_type == 0, "cf1_pin")
            yr.sensor(sensor)

        case 2:  # HLW8032
            yr.warn("HLW8032 is not supported")

        case 3:  # BL0942
            rx_pin = config.get("ele_rx", None)
            tx_pin = config.get("ele_tx", None)
            rx_pin = f"P{rx_pin}" if rx_pin else "RX1"
            tx_pin = f"P{tx_pin}" if tx_pin else "TX1"
            chip = "BL0942"
            yr.log(f"Power monitoring chip {chip}: " f"RX={rx_pin}, TX={tx_pin}")
            yr.found = True
            uart = {
                "id": "uart_bus",
                "tx_pin": tx_pin,
                "rx_pin": rx_pin,
                "baud_rate": 4800,
                "stop_bits": 1,
            }
            yr.data["uart"] = uart
            sensor = {
                "platform": "bl0942",
                "uart_id": uart["id"],
                "current": {"name": f"{chip} Current"},
                "voltage": {"name": f"{chip} Voltage"},
                "power": {"name": f"{chip} Power", "filters": {"multiply": -1}},
                "energy": {"name": f"{chip} Energy"},
                "frequency": {"name": f"{chip} Frequency", "accuracy_decimals": 2},
            }
            yr.sensor(sensor)

        case _:
            yr.warn(f"Unrecognized power monitoring chip {chip_type}")
