#  Copyright (c) Kuba Szczodrzyński 2023-8-28.

import requests


def cloudcutter_list_devices() -> tuple[list[str], list[str]]:
    url = "https://tuya-cloudcutter.github.io/api/devices.json"
    with requests.get(url) as r:
        if r.status_code != 200:
            raise RuntimeError(
                "Couldn't download Cloudcutter device list.\n"
                f"Status code: {r.status_code}"
            )
        devices = r.json()

    for device in devices:
        device["name"] = f'{device["manufacturer"]} - {device["name"]}'
    devices = sorted(devices, key=lambda d: d["name"])

    devices_slug = [device["slug"] for device in devices]
    devices_name = [device["name"] for device in devices]

    return devices_slug, devices_name


def cloudcutter_get_device(slug: str) -> dict:
    url = f"https://tuya-cloudcutter.github.io/api/devices/{slug}.json"
    with requests.get(url) as r:
        if r.status_code != 200:
            raise RuntimeError(
                f"Couldn't download Cloudcutter device '{slug}'.\n"
                f"Status code: {r.status_code}"
            )
        device = r.json()
        for i, profile in enumerate(device["profiles"]):
            device["profiles"][i] = cloudcutter_get_profile(profile["slug"])
    return device


def cloudcutter_get_profile(slug: str) -> dict:
    url = f"https://tuya-cloudcutter.github.io/api/profiles/{slug}.json"
    with requests.get(url) as r:
        if r.status_code != 200:
            raise RuntimeError(
                f"Couldn't download Cloudcutter profile '{slug}'.\n"
                f"Status code: {r.status_code}"
            )
        profile = r.json()
    return profile
