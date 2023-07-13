#  Copyright (c) Kuba Szczodrzyński 2023-4-22.

from dataclasses import dataclass


@dataclass
class Opts:
    esphome_block: bool = True
    name_mac: bool = False
    common: bool = True
    web_server: bool = True
    restart: bool = False
    uptime: bool = False
    lt_version: bool = True
    wifi_ssid: str = ""
    wifi_password: str = ""
    ota_password: str = ""
    api_password: str = ""
