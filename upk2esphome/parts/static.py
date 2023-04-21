#  Copyright (c) Kuba Szczodrzyński 2023-4-21.

from upk2esphome.result import YamlResult


def generate(yr: YamlResult, config: dict):
    yr.data["logger"] = {}
    yr.data["web_server"] = {}
    yr.data["captive_portal"] = {}
    yr.data["mdns"] = {}
    yr.data["api"] = {"password": ""}
    yr.data["ota"] = {"password": ""}
    yr.data["wifi"] = {
        "ssid": "!secret wifi_ssid",
        "password": "!secret wifi_password",
        "ap": {},
    }
    yr.data["button"] = [
        {
            "platform": "restart",
            "name": "Restart",
        }
    ]
    yr.sensor(
        {
            "platform": "uptime",
            "name": "Uptime",
        }
    )
