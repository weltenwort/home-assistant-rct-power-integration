"""Tests for async_get_data retry behaviour."""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest

from custom_components.rct_power.lib.api import (
    RETRY_DELAY_LONG,
    RctPowerApiClient,
)


@pytest.fixture()
def client() -> RctPowerApiClient:
    return RctPowerApiClient(hostname="127.0.0.1", port=8899)


async def test_allow_long_retry_false_never_waits_300s(
    client: RctPowerApiClient,
) -> None:
    """When allow_long_retry=False, the 300s sleep must never be awaited and the
    call must raise quickly (only quick-retry delays apply)."""
    sleep_calls: list[float] = []

    async def fake_sleep(delay: float) -> None:
        sleep_calls.append(delay)

    with (
        patch.object(
            client,
            "_connect_and_read",
            new=AsyncMock(side_effect=TimeoutError("unreachable")),
        ),
        patch(
            "custom_components.rct_power.lib.api.asyncio.sleep", side_effect=fake_sleep
        ),
    ):
        with pytest.raises((TimeoutError, OSError)):
            await client.async_get_data([0x12345678], allow_long_retry=False)

    assert RETRY_DELAY_LONG not in sleep_calls, (
        f"300s sleep was awaited with allow_long_retry=False; sleep calls: {sleep_calls}"
    )


async def test_allow_long_retry_true_does_wait_300s(client: RctPowerApiClient) -> None:
    """When allow_long_retry=True (default), the 300s sleep IS awaited after quick retries
    are exhausted."""
    sleep_calls: list[float] = []

    async def fake_sleep(delay: float) -> None:
        sleep_calls.append(delay)

    with (
        patch.object(
            client,
            "_connect_and_read",
            new=AsyncMock(side_effect=TimeoutError("unreachable")),
        ),
        patch(
            "custom_components.rct_power.lib.api.asyncio.sleep", side_effect=fake_sleep
        ),
    ):
        with pytest.raises((TimeoutError, OSError)):
            await client.async_get_data([0x12345678], allow_long_retry=True)

    assert RETRY_DELAY_LONG in sleep_calls, (
        f"Expected the {RETRY_DELAY_LONG}s sleep but got: {sleep_calls}"
    )


async def test_get_serial_number_allow_long_retry_false_never_waits_300s(
    client: RctPowerApiClient,
) -> None:
    """get_serial_number(allow_long_retry=False) must not do the long wait."""
    sleep_calls: list[float] = []

    async def fake_sleep(delay: float) -> None:
        sleep_calls.append(delay)

    with (
        patch.object(
            client,
            "_connect_and_read",
            new=AsyncMock(side_effect=TimeoutError("unreachable")),
        ),
        patch(
            "custom_components.rct_power.lib.api.asyncio.sleep", side_effect=fake_sleep
        ),
    ):
        with pytest.raises((TimeoutError, OSError)):
            await client.get_serial_number(allow_long_retry=False)

    assert RETRY_DELAY_LONG not in sleep_calls, (
        f"300s sleep was awaited via get_serial_number(allow_long_retry=False); "
        f"sleep calls: {sleep_calls}"
    )
