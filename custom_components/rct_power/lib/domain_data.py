from typing import Any, Dict, cast

from homeassistant.core import HomeAssistant

from .const import DOMAIN

RctPowerDomainData = Dict[str, Any]


def get_domain_data(home_assistant: HomeAssistant) -> RctPowerDomainData:
    data = cast(Dict[Any, Any], home_assistant.data)  # type: ignore

    return data.setdefault(DOMAIN, {})
