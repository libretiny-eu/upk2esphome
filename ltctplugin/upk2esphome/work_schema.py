#  Copyright (c) Kuba Szczodrzyński 2023-9-5.

from logging import debug
from typing import Callable

import requests
from ltchiptool.gui.work.base import BaseThread

from upk2esphome.const import SCHEMA_PULL_URL, SCHEMA_URL_PREFIX

SCHEMA_PULL_USER = "upk-ltchiptool-v1"
SCHEMA_PULL_PASS = "70b5d7b24cfbba7c0ca831d337c99b37"


class UpkSchemaThread(BaseThread):
    def __init__(
        self,
        device: dict,
        software: dict | None,
        license_: dict | None,
        schema_id: str | None,
        on_success: Callable[[dict], None] = None,
        on_error: Callable[[str], None] = None,
    ):
        super().__init__()
        self.device = device or {}
        self.software = software or {}
        self.license = license_ or {}
        self.schema_id = schema_id
        self.on_success = on_success
        self.on_error = on_error

    def run_impl(self):
        auth = (SCHEMA_PULL_USER, SCHEMA_PULL_PASS)
        if self.schema_id:
            debug(f"Schema: schema_id={self.schema_id}")
            with requests.get(url=SCHEMA_URL_PREFIX + self.schema_id, auth=auth) as r:
                if r.status_code == 200:
                    debug(f"Schema: found model by ID")
                    self.on_success(r.json())
                    return

        debug(f"Schema: device={self.device}")
        debug(f"Schema: software={self.software}")
        debug(f"Schema: license={self.license}")
        if (
            not self.device.get("firmwareKey", None)
            and not self.device.get("productKey", None)
            and not self.device.get("factoryPin", None)
        ):
            self.on_error("Missing FK/PK/FC")
            return
        if self.license.get("uuid", None) and not self.license.get("authKey", None):
            self.on_error("Missing License Auth Key")
            return
        if not self.license.get("uuid", None) and self.license.get("authKey", None):
            self.on_error("Missing License UUID")
            return

        data = dict(
            device=self.device,
            software=self.software,
            license=self.license,
        )
        with requests.post(url=SCHEMA_PULL_URL, json=data, auth=auth) as r:
            if r.status_code != 200:
                self.on_error(
                    r.json().get("message", f"Response status code {r.status_code}"),
                )
                return
            self.on_success(r.json())
