#  Copyright (c) Kuba Szczodrzyński 2023-4-21.

import re

import yaml

from upk2esphome.config import ConfigData


class MyDumper(yaml.Dumper):
    def increase_indent(self, flow=False, **_):
        return super(MyDumper, self).increase_indent(flow, False)


class YamlResult:
    data: dict
    logs: list[str]
    warnings: list[str]
    errors: list[str]
    found: bool
    config: ConfigData | None
    needs_tuyamcu_model: bool

    def __init__(self):
        self.data = {}
        self.logs = []
        self.warnings = []
        self.errors = []
        self.found = False
        self.config = None
        self.needs_tuyamcu_model = False

    @property
    def text(self) -> str:
        text = yaml.dump(self.data, sort_keys=False, Dumper=MyDumper)
        text = re.sub(r"'!(\w+) (.+)'", r"!\1 \2", text)
        text = re.sub(r"\n([a-z])", r"\n\n\1", text)
        text = text.replace("'", '"')
        text = re.sub(r'_\d+: "(.+?)"', r"# \1", text)
        text = text.replace(" {}", "")
        text = text.replace("{}", "")
        return text

    def log(self, text: str):
        self.logs.append(text)

    def warn(self, text: str):
        self.warnings.append(text)

    def error(self, text: str):
        self.errors.append(text)

    def component(self, data: dict):
        if "external_components" not in self.data:
            self.data["external_components"] = []
        self.data["external_components"].append(data)

    def output(self, data: dict):
        if "output" not in self.data:
            self.data["output"] = []
        self.data["output"].append(data)

    def light(self, data: dict):
        if "light" not in self.data:
            self.data["light"] = []
        self.data["light"].append(data)

    def switch(self, data: dict):
        if "switch" not in self.data:
            self.data["switch"] = []
        self.data["switch"].append(data)

    def binary(self, data: dict):
        if "binary_sensor" not in self.data:
            self.data["binary_sensor"] = []
        self.data["binary_sensor"].append(data)

    def sensor(self, data: dict):
        if "sensor" not in self.data:
            self.data["sensor"] = []
        self.data["sensor"].append(data)

    def text_sensor(self, data: dict):
        if "text_sensor" not in self.data:
            self.data["text_sensor"] = []
        self.data["text_sensor"].append(data)

    def button(self, data: dict):
        if "button" not in self.data:
            self.data["button"] = []
        self.data["button"].append(data)

    def number(self, data: dict):
        if "number" not in self.data:
            self.data["number"] = []
        self.data["number"].append(data)

    def select(self, data: dict):
        if "select" not in self.data:
            self.data["select"] = []
        self.data["select"].append(data)

    def tuya_on_datapoint_update(self, data: dict):
        if "tuya" not in self.data:
            self.data["tuya"] = tuya = {}
        else:
            tuya = self.data["tuya"]
        if "on_datapoint_update" not in tuya:
            tuya["on_datapoint_update"] = []
        tuya["on_datapoint_update"].append(data)
