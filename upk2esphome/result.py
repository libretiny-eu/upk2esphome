#  Copyright (c) Kuba Szczodrzyński 2023-4-21.


class YamlResult:
    data: dict
    text: str
    logs: list[str]
    warnings: list[str]

    def __init__(self):
        self.data = {}
        self.text = ""
        self.logs = []
        self.warnings = []

    def log(self, text: str):
        self.logs.append(text)

    def warn(self, text: str):
        self.warnings.append(text)

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
