#  Copyright (c) Kuba Szczodrzyński 2023-5-20.

from typing import Any, Dict

from ltctplugin.base import PluginBase
from semantic_version.base import BaseSpec, SimpleSpec


class Plugin(PluginBase):
    @property
    def title(self) -> str:
        return "UPK2ESPHome"

    @property
    def ltchiptool_version(self) -> BaseSpec | None:
        return SimpleSpec(">=4.4.0")

    @property
    def has_cli(self) -> bool:
        return True

    @property
    def has_gui(self) -> bool:
        return True

    def build_cli(self, *args, **kwargs) -> Dict[str, Any]:
        from .cli import cli

        return dict(
            upk2esphome=cli,
        )

    def build_gui(self, *args, **kwargs) -> Dict[str, Any]:
        from .gui import UpkPanel

        return dict(
            upk=UpkPanel,
        )


entrypoint = Plugin

__all__ = [
    "entrypoint",
]
