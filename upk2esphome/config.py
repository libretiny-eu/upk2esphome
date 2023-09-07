#  Copyright (c) Kuba Szczodrzyński 2023-9-4.

from dataclasses import dataclass
from enum import Enum
from typing import Literal


@dataclass
class ConfigData:
    type: "Type"
    data: dict
    extras: dict

    class Type(Enum):
        CLOUDCUTTER = "Cloudcutter JSON"
        STORAGE = "Storage JSON"
        RAW = "Raw UPK"

    @staticmethod
    def build(data: dict, extras: dict) -> "ConfigData":
        if "schemas" in data and "profiles" in data:
            type = ConfigData.Type.CLOUDCUTTER
        elif "gw_bi" in data:
            type = ConfigData.Type.STORAGE
        elif "Jsonver" in data or "jv" in data or "crc" in data:
            type = ConfigData.Type.RAW
            data = dict(sorted(data.items()))
        else:
            raise ValueError("Couldn't recognize input data")
        return ConfigData(type, data, extras)

    @property
    def is_tuya_mcu(self) -> bool:
        match self.type:
            case ConfigData.Type.CLOUDCUTTER:
                slug = self.profile_slug or ""
                return slug.startswith("bk7231") and "common" in slug
            case ConfigData.Type.STORAGE:
                return "baud_cfg" in self.data or "uart_adapt_params" in self.data
            case ConfigData.Type.RAW:
                return False

    @property
    def upk(self) -> dict:
        match self.type:
            case ConfigData.Type.CLOUDCUTTER:
                return self.data.get("device_configuration", {})
            case ConfigData.Type.STORAGE:
                return self.data.get("user_param_key", {})
            case ConfigData.Type.RAW:
                return self.data

    @property
    def uart_config(self) -> dict:
        return self.data.get("baud_cfg", {}) or self.data.get("uart_adapt_params", {})

    @property
    def model(self) -> dict:
        return self.extras.get("model", {})

    @property
    def category(self) -> str | None:
        return self.extras.get("category", {})

    @property
    def profile(self) -> dict | None:
        profiles = self.data.get("profiles", [])
        profile = profiles and profiles[0] or {}
        if isinstance(profile, dict):
            return profile
        return None

    @property
    def profile_slug(self) -> str | None:
        profiles = self.data.get("profiles", [])
        profile = profiles and profiles[0] or {}
        if isinstance(profile, str):
            return profile.lower()
        slug = profile.get("slug", None)
        return slug and slug.lower()

    @property
    def chip_name(
        self,
    ) -> Literal["BK7231T"] | Literal["BK7231N"] | Literal["?"] | None:
        module = self.upk.get("module", "")
        if module:
            match module[0:2]:
                case "WB":
                    return "BK7231T"
                case "CB":
                    return "BK7231N"
                case _:
                    return "?"
        profile = self.profile
        if profile and "firmware" in profile:
            chip = profile["firmware"].get("chip", None)
            if chip == "BK7231T":
                return "BK7231T"
            if chip == "BK7231N":
                return "BK7231N"
        slug = self.profile_slug
        if slug:
            if "bk7231t" in slug:
                return "BK7231T"
            if "bk7231s" in slug:
                return "BK7231T"
            if "bk7231n" in slug:
                return "BK7231N"
        if self.type == ConfigData.Type.STORAGE:
            if "uart_adapt_params" in self.data:
                return "BK7231T"
            if "baud_cfg" in self.data:
                return "BK7231N"
        return None

    @property
    def schema_id(self) -> str | None:
        match self.type:
            case ConfigData.Type.CLOUDCUTTER:
                return list(self.data.get("schemas", {}) or [None])[0]
            case ConfigData.Type.STORAGE:
                return self.data.get("gw_di", {}).get("s_id", None)

    @property
    def data_device(self) -> dict | None:
        match self.type:
            case ConfigData.Type.CLOUDCUTTER:
                key = self.data.get("key", None)
                return dict(
                    firmwareKey=key if key.startswith("key") else None,
                    productKey=key if not key.startswith("key") else None,
                    factoryPin=None,
                    softwareVer=self.profile.get("firmware", {}).get("version", None),
                )
            case ConfigData.Type.STORAGE:
                gw_di = self.data.get("gw_di", {})
                gw_bi = self.data.get("gw_bi", {})
                pk = gw_di.get("pk", None)
                return dict(
                    firmwareKey=gw_di.get("firmk", None),
                    productKey=pk if not pk.startswith("key") else None,
                    factoryPin=gw_bi.get("fac_pin", None),
                    softwareVer=gw_di.get("swv", None),
                )

    @property
    def data_software(self) -> dict | None:
        if self.type != ConfigData.Type.STORAGE:
            return None
        gw_di = self.data.get("gw_di", {})
        return dict(
            bv=gw_di.get("bv", None),
            pv=gw_di.get("pv", None),
            cadv=gw_di.get("cadv", None),
            cdv=gw_di.get("cdv", None),
        )

    @property
    def data_license(self) -> dict | None:
        if self.type != ConfigData.Type.STORAGE:
            return None
        gw_bi = self.data.get("gw_bi", {})
        if gw_bi.get("ap_ssid", "") == "A":
            return None
        return dict(
            uuid=gw_bi.get("uuid", None),
            authKey=gw_bi.get("auth_key", None),
        )
