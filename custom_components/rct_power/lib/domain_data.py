from __future__ import annotations

from typing import Any, cast

from homeassistant.core import HomeAssistant

from .const import DOMAIN

RctPowerDomainData = dict[str, Any]


def get_domain_data(home_assistant: HomeAssistant) -> RctPowerDomainData:
    data = cast(dict[Any, Any], home_assistant.data)  # type: ignore

    return data.setdefault(DOMAIN, {})
