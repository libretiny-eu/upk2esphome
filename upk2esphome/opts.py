#  Copyright (c) Kuba Szczodrzyński 2023-4-22.

from dataclasses import dataclass


@dataclass
class Opts:
    esphome_block: bool = True
    name_mac: bool = True
    common: bool = True
    web_server: bool = True
    restart: bool = True
    uptime: bool = True
    lt_version: bool = True
    wifi_ssid: str = ""
    wifi_password: str = ""
    ota_password: str = ""
    api_password: str = ""
