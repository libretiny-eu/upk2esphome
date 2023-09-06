#  Copyright (c) Kuba Szczodrzyński 2023-9-6.

from dataclasses import dataclass
from enum import Enum
from typing import Literal


@dataclass
class Datapoint:
    id: int
    code: str
    mode: Literal["rw"] | Literal["ro"] | Literal["wo"]
    name: str
    description: str
    spec: "Datapoint.Spec"

    @dataclass
    class Spec:
        type: "Datapoint.Spec.Type"
        max: int = None
        min: int = None
        scale: int = None
        step: int = None
        unit: str = None
        maxlen: int = None
        label: list[str] = None
        range: list[str] = None
        typeDefaultValue: int | bool | str = None

        class Type(Enum):
            BOOL = "bool"
            VALUE = "value"
            ENUM = "enum"
            BITMAP = "bitmap"
            STRING = "string"
            RAW = "raw"

    @staticmethod
    def build(dp: dict) -> "Datapoint":
        spec = dp.get("typeSpec", None)
        spec["type"] = Datapoint.Spec.Type(spec["type"])
        return Datapoint(
            id=dp.get("abilityId"),
            code=dp.get("code"),
            mode=dp.get("accessMode"),
            name=dp.get("name"),
            description=dp.get("description"),
            spec=spec and Datapoint.Spec(**spec),
        )

    @property
    def info(self) -> str:
        return (
            f"DP {self.id}, "
            f"{self.spec.type.name}({self.mode}), "
            f"{self.code} ({self.name})"
        )
