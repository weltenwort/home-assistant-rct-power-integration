"""Sample API Client."""
from asyncio import StreamReader, StreamWriter, open_connection, TimeoutError
from asyncio.locks import Lock
import logging
import socket
from typing import Any, Dict, List, Optional

import async_timeout
from homeassistant.helpers.update_coordinator import UpdateFailed
from rctclient.frame import ReceiveFrame, SendFrame
from rctclient.registry import REGISTRY
from rctclient.types import Command, FrameType
from rctclient.utils import decode_value

CONNECTION_TIMEOUT = 20
READ_TIMEOUT = 20

_LOGGER: logging.Logger = logging.getLogger(__package__)

INVERTER_SN_OID = 0x7924ABD9

RctPowerData = Dict[int, Any]


class RctPowerApiClient:
    def __init__(self, hostname: str, port: int) -> None:
        """Sample API Client."""
        self._hostname = hostname
        self._port = port

        # ensure only one connection at a time is established because the
        # inverter's firmware doesn't handle it well at the time of writing
        self._connection_lock = Lock()

    async def get_serial_number(self) -> Optional[str]:
        inverter_data = await self.async_get_data([INVERTER_SN_OID])

        return inverter_data.get(INVERTER_SN_OID)

    async def async_get_data(self, object_ids: List[int]) -> Optional[RctPowerData]:
        async with self._connection_lock:
            async with async_timeout.timeout(CONNECTION_TIMEOUT):
                reader, writer = await open_connection(
                    host=self._hostname, port=self._port
                )

                try:
                    if reader.at_eof():
                        raise UpdateFailed("Read stream closed")

                    return {
                        object_id: await self._read_object(
                            reader=reader, writer=writer, object_id=object_id
                        )
                        for object_id in object_ids
                    }
                finally:
                    writer.close()

    async def _read_object(
        self, reader: StreamReader, writer: StreamWriter, object_id: int
    ):
        read_command_frame = SendFrame(command=Command.READ, id=object_id)
        response_frame = ReceiveFrame()

        _LOGGER.debug("Requesting RCT Power data for object %x...", object_id)

        async with async_timeout.timeout(READ_TIMEOUT):
            await writer.drain()
            writer.write(read_command_frame.data)

            while not response_frame.complete() and not reader.at_eof():
                raw_response = await reader.read(256)

                if len(raw_response) > 0:
                    response_frame.consume(raw_response)

        if response_frame.is_complete():
            return decode_value(REGISTRY.type_by_id(object_id), response_frame.data)
