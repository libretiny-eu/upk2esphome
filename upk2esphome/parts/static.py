#  Copyright (c) Kuba Szczodrzyński 2023-4-21.

from upk2esphome.opts import Opts
from upk2esphome.result import YamlResult


def generate(yr: YamlResult, config: dict, opts: Opts):
    if opts.common:
        yr.data["logger"] = {}
    if opts.web_server:
        yr.data["web_server"] = {}
        yr.data["captive_portal"] = {}
        yr.data["mdns"] = {}
    if opts.common:
        yr.data["api"] = {"password": opts.api_password}
        yr.data["ota"] = {"password": opts.ota_password}
        yr.data["wifi"] = {
            "ssid": opts.wifi_ssid,
            "password": opts.wifi_password,
            "ap": {},
        }
    if opts.restart:
        yr.button(
            {
                "platform": "restart",
                "name": "Restart",
            }
        )
        yr.data["debug"] = {
            "update_interval": "30s",
        }
        yr.text_sensor(
            {
                "platform": "debug",
                "reset_reason": {"name": "Reset Reason"},
            }
        )
    if opts.uptime:
        yr.sensor(
            {
                "platform": "uptime",
                "name": "Uptime",
            }
        )
    if opts.lt_version:
        yr.text_sensor(
            {
                "platform": "libretiny",
                "version": {"name": "LibreTiny Version"},
            }
        )
