from __future__ import annotations
import logging
from typing import Any
from dataclasses import dataclass
from PyQt5.QtCore import QSettings


@dataclass
class DefaultSetting:
    """Default settings."""
    settings: QSettings
    group_name: str
    name: str
    value: Any

    def set(self, value) -> None:
        """Set the default setting."""
        self.value = value
        self.settings.beginGroup(self.group_name)
        self.settings.setValue(self.name, self.value)
        self.settings.endGroup()

    def initialize_setting(self) -> DefaultSetting:
        """Initialize the default setting or pulls the current setting value."""
        self.settings.beginGroup(self.group_name)
        if not self.settings.contains(self.name):
            self.settings.setValue(self.name, self.value)
        else:
            self.value = self.settings.value(self.name)
        self.settings.endGroup()
        return self


@dataclass
class LabelData:
    """Label data."""
    barcode: str
    part_number: str
    part_description: str
    quantity: int
    material_thickness: str

    def __str__(self) -> str:
        """Return the label data as a string."""
        return f'barcode="{self.barcode}", part_number="{self.part_number}", part_description="{self.part_description}", quantity="{self.quantity}", material_thickness="{self.material_thickness}"'