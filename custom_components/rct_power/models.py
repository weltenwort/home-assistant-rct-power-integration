from __future__ import annotations

from typing import TypedDict


class RctConfEntryData(TypedDict):
    hostname: str
    port: int


class RctConfEntryOptions(TypedDict, total=False):
    frequent_scan_interval: int
    infrequent_scan_interval: int
    static_scan_interval: int
